export type ITag = '家' | '公司' | '学校' | '超市'
export interface IRenderTableList {
    date: string
    name: string
    address: string
    tag: ITag
    amt: number
}