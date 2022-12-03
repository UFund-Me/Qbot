import { format, unformat } from '/@/utils/tools'

describe('tools', () => {
    it('format', () => {
        expect(format(15.693)).toBe('￥15.69')
        expect(format('15.693')).toBe('￥15.69')
        expect(format('qwe')).toBe('￥0.00')
        expect(format('15.693', '$')).toBe('$15.69')
        expect(format('36915.693')).toBe('￥36,915.69')
        expect(format('1236915.693')).toBe('￥1,236,915.69')
    })
    it('unformat', () => {
        expect(unformat('￥15.69')).toBe(15.69)
        expect(unformat('$15.69')).toBe(15.69)
        expect(unformat('￥36,915.69')).toBe(36915.69)
        expect(unformat('￥1,236,915.69')).toBe(1236915.69)
    })
})

