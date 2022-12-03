import { createProdMockServer } from 'vite-plugin-mock/es/createProdMockServer'

import testModule from '/mock/index'

export function setupProdMockServer():void {
    createProdMockServer([...testModule])
}