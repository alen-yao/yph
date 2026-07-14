/**
 * 移动端 rem 适配方案
 * 基准值：750px 设计稿，根字体大小为 37.5px (750 / 20 = 37.5)
 * 实际字体大小 = 设备宽度 / 20
 */

const baseSize = 37.5

function setRem() {
  // 获取设备宽度
  const clientWidth = document.documentElement.clientWidth || document.body.clientWidth

  // 限制最大宽度为 750px（避免在大屏设备上字体过大）
  const width = Math.min(clientWidth, 750)

  // 计算并设置根字体大小
  const scale = width / 750
  const fontSize = baseSize * scale

  document.documentElement.style.fontSize = fontSize + 'px'
}

// 初始化
setRem()

// 监听窗口大小变化
window.addEventListener('resize', setRem)
window.addEventListener('orientationchange', setRem)

export default setRem
