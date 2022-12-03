import { Ref, nextTick } from 'vue'
interface IAnimate {
    timing(p: number): number
    draw(p: number): void
    duration: number
}
export function animate(param:IAnimate):void {
    const { timing, draw, duration } = param
    const start = performance.now()
    requestAnimationFrame(function animate(time) {
        // timeFraction 从 0 增加到 1
        let timeFraction = (time - start) / duration
        if (timeFraction > 1) timeFraction = 1
  
        // 计算当前动画状态，百分比，0-1
        const progress = timing(timeFraction)
  
        draw(progress) // 绘制
  
        if (timeFraction < 1) {
            requestAnimationFrame(animate)
        }
    })
}
/**
 * 下拉动画，0=>auto，auto=>0
 * @param el dom节点
 * @param isShow 是否显示
 * @param duration 持续时间
 */
export async function slide(el:Ref<HTMLDivElement | null>, isShow:boolean, duration = 200):Promise<void> {
    if(!el.value) return
    const { position, zIndex } = getComputedStyle(el.value)
    if(isShow) {
        el.value.style.position = 'absolute'
        el.value.style.zIndex = '-100000'
        el.value.style.height = 'auto'
    }
    await nextTick()
    const height = el.value.offsetHeight
    if(isShow) {
        el.value.style.position = position
        el.value.style.zIndex = zIndex
        el.value.style.height = '0px'
    }
    animate({
        timing: timing.linear,
        draw: function(progress) {
            if(!el.value) return
            el.value.style.height = isShow 
                ? progress === 1
                    ? 'auto'
                    : (`${progress * height}px`) 
                : progress === 0
                    ? 'auto'
                    : (`${(1 - progress) * height}px`)
        },
        duration: duration
    })
}

const timing = {
    // 线性
    linear(timeFraction: number): number {
        return timeFraction
    },
    // n 次幂
    quad(timeFraction: number, n = 2): number {
        return Math.pow(timeFraction, n)
    },
    // 圆弧
    circle(timeFraction: number): number {
        return 1 - Math.sin(Math.acos(timeFraction))
    }
}