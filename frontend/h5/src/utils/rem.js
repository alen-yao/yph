/**
 * 移动端 rem 适配方案
 * 基准值：750px 设计稿，根字体大小为 37.5px (750 / 20 = 37.5)
 * 实际字体大小 = 设备宽度 / 20
 */

const BASE_WIDTH = 375
const BASE_FONT_SIZE = 37.5

function setRem() {
  // 获取设备宽度
  const clientWidth = document.documentElement.clientWidth || document.body.clientWidth || BASE_WIDTH

  // 以 375px 为基准，并限制大屏 H5 的最大布局宽度。
  const width = Math.min(clientWidth, BASE_WIDTH)
  const fontSize = (width / BASE_WIDTH) * BASE_FONT_SIZE

  document.documentElement.style.fontSize = `${fontSize}px`
}

// 初始化
setRem()

// 监听窗口大小变化
window.addEventListener('resize', setRem)
window.addEventListener('orientationchange', setRem)

export default setRem
