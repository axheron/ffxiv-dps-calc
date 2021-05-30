import { FloorPipe } from './floor.pipe';

describe('FloorPipe', () => {
	const pipe = new FloorPipe();

	it('floors a decimal number towards zero', () => {
		expect(pipe.transform(1234.56)).toBe(1234);
	});
});
