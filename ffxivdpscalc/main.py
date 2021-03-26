# shitty proof of concept. run the run_test() method to try it (and maybe change some values).
# todo: break this out into files properly

from enum import Enum, auto
import math

class Stats(Enum):
  MAINSTAT = (340, 165, 0)
  DET = (340, 130, 0)
  CRIT = (380, 200, 400)
  DH = (380, 1250, 0)
  SPEED = (380, 130, 0)
  TEN = (380, 100, 0)
  PIE = (340, 1, 0)
  GCD = (2500, 1, 0) # in milliseconds
  PRECISION = (1000, 1, 0) # defaulting to 3 digits of precision

  def __init__(self, base, m_factor, m_scalar):
    self.base = base
    self.m_factor = m_factor
    self.m_scalar = m_scalar

class Stat():
  def __init__(self, stat, value):
    self.stat = stat
    self.value = value
  
  def get_multiplier(self):
    if self.stat == Stats.DH:
      return 1.25
    
    magic_num = 3300
    if self.stat == Stats.MAINSTAT: 
      magic_num = 340 # don't ask me why dude
    delta = self.value - self.stat.base
    return self.stat.m_factor * delta // magic_num + self.stat.m_scalar

class ProbabalisticStat(Stat):
  def __init__(self, stat, value):
    super().__init__(stat, value)
    self.p_factor = 1
    self.p_scalar = 0
    if stat == Stats.CRIT:
      self.p_factor = 200
      self.p_scalar = 50
    elif stat == Stats.DH:
      self.p_factor = 550
  
  def get_p(self):
    delta = self.value - self.stat.base
    return  (self.p_factor * delta // 3300 + self.p_scalar) / Stats.PRECISION.base

class CharacterStats:
  def __init__(self, job, wd, mainstat, det, crit, dh, speed, ten, pie):
    self.job = job
    self.wd = wd
    self.mainstat = Stat(Stats.MAINSTAT, mainstat)
    self.det = Stat(Stats.DET, det)
    self.crit = ProbabalisticStat(Stats.CRIT, crit)
    self.dh = ProbabalisticStat(Stats.DH, dh)
    self.speed = Stat(Stats.SPEED, speed)
    self.ten = Stat(Stats.TEN, ten)
    self.pie = Stat(Stats.PIE, pie)

  @classmethod
  def truncate(cls, val, precision=1000):
    return (precision + val) / precision

  @classmethod
  def multiply_and_truncate(cls, val, factor, precision=1000):
    return math.floor(val * cls.truncate(factor, precision))

  @classmethod
  def apply_stat(cls, damage, stat):
    return cls.multiply_and_truncate(damage, stat.get_multiplier())

  # comp is a Comp() object
  def calc_damage(self, potency, comp, is_dot=False, crit_rate=None, dh_rate=None):
    # modify mainstat according to number of roles
    modified_mainstat = Stat(Stats.MAINSTAT, math.floor(self.mainstat.value * (1 + 0.01 * comp.n_roles)))

    # damage effect of non-probabalistic stats
    damage = potency * (self.wd + (340 * self.job.job_mod // 1000)) * (100 + modified_mainstat.get_multiplier()) // 100; # cursed tbh
    damage = self.apply_stat(damage, self.det)
    damage = self.apply_stat(damage, self.ten)
    if is_dot: damage = self.apply_stat(damage, self.speed)

    damage //= 100 # why? i do not know. cargo culted

    # damage effect of job traits / stance
    # todo: pull out traits
    if self.job.role == Roles.HEALER: damage = math.floor(damage * 1.3) # magic and mend 

    # todo: effect of raid buffs

    # damage effect of probabalistic stats 
    crit_damage = self.apply_stat(damage, self.crit)
    dh_damage = damage * self.dh.stat.m_factor // 1000
    cdh_damage = crit_damage * self.dh.stat.m_factor // 1000

    # use expected crit rate based on stats if none is supplied
    if not crit_rate: crit_rate = self.crit.get_p()
    if not dh_rate: dh_rate = self.dh.get_p()

    # apply party crit/dh buffs
    for buff in comp.raidbuffs:
      if buff in Buffs.crit_buffs():
        crit_rate += buff.avg_buff_effect()
      elif buff in Buffs.dh_buffs():
        dh_rate += buff.avg_buff_effect()
    
    cdh_rate = crit_rate * dh_rate
    normal_rate = 1 - crit_rate - dh_rate + cdh_rate
    return damage * normal_rate + crit_damage * (crit_rate - cdh_rate) + dh_damage * (dh_rate - cdh_rate) + cdh_damage * cdh_rate

class Roles(Enum):
  TANK = auto()
  HEALER = auto()
  MELEE = auto()
  RANGED = auto()
  CASTER = auto()

class Buffs(Enum):
  # aoe
  CHAIN = (0.1, 15, 120)
  DIV = (0.06, 15, 120) # 3 seal div
  TRICK = (0.05, 15, 60)
  LITANY = (0.1, 20, 180)
  BROTHERHOOD = (0.05, 15, 90)
  BV = (0.2, 20, 180)
  BARD_CRIT = (0.02, 30, 80)
  BARD_DH = (0.03, 20, 80)
  TECH = (0.05, 20, 120)
  DEVOTION = (0.05, 15, 180)
  EMBOLDEN = (0.1, 20, 120) # need to handle buff decay
  # single target
  CARD = (0.06, 15, 30)
  LORD_LADY = (0.08, 15, 30)
  DSIGHT_SELF = (0.1, 20, 120)
  DSIGHT_OTHER = (0.05, 20, 120)
  DEVILMENT = (0.2, 20, 120)
  # todo: should probably add standard, personal tank buffs

  def __init__(self, multiplier, duration, cd):
    self.multiplier = multiplier
    self.duration = duration
    self.cd = cd

  @classmethod
  def crit_buffs(cls):
    return {cls.CHAIN, cls.LITANY, cls.DEVILMENT, cls.BARD_CRIT}

  @classmethod
  def dh_buffs(cls):
    return {cls.BV, cls.BARD_DH, cls.DEVILMENT}

  def avg_buff_effect(self):
    return self.multiplier * self.duration / self.cd

class Jobs(Enum):
  # job modifiers from https://www.akhmorning.com/allagan-studies/modifiers/
  SCH = (115, Roles.HEALER, [Buffs.CHAIN])
  AST = (115, Roles.HEALER, [Buffs.DIV])
  WHM = (115, Roles.HEALER, [])
  PLD = (110, Roles.TANK, [])
  WAR = (110, Roles.TANK, [])
  DRK = (110, Roles.TANK, [])
  GNB = (110, Roles.TANK, [])
  NIN = (110, Roles.MELEE, [Buffs.TRICK])
  DRG = (115, Roles.MELEE, [Buffs.LITANY])
  MNK = (110, Roles.MELEE, [Buffs.BROTHERHOOD])
  SAM = (112, Roles.MELEE, [])
  MCH = (115, Roles.RANGED, [])
  DNC = (115, Roles.RANGED, [Buffs.TECH])
  BRD = (115, Roles.RANGED, [Buffs.BV, Buffs.BARD_CRIT, Buffs.BARD_DH])
  SMN = (115, Roles.CASTER, [Buffs.DEVOTION])
  BLM = (115, Roles.CASTER, [])
  RDM = (115, Roles.CASTER, [Buffs.EMBOLDEN])

  def __init__(self, job_mod, role, raidbuff):
    self.job_mod = job_mod
    self.role = role
    self.raidbuff = raidbuff

class Comp():
  def __init__(self, jobs):
    self.jobs = jobs

    self.raidbuffs = set()
    has_tank = 0
    has_healer = 0
    has_melee = 0
    has_ranged = 0
    has_caster = 0
    for job in jobs:
      for buff in job.raidbuff: self.raidbuffs.add(buff)

      if job.role == Roles.TANK: has_tank = 1
      elif job.role == Roles.HEALER: has_healer = 1
      elif job.role == Roles.MELEE: has_melee = 1
      elif job.role == Roles.RANGED: has_ranged = 1
      elif job.role == Roles.CASTER: has_caster = 1
    self.n_roles = has_tank + has_healer + has_melee + has_ranged + has_caster

