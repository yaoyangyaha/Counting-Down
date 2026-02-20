<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const username = ref(null)
const myPoints = ref(0)
const loggedIn = computed(() => !!username.value)

/* ================= 滑块 ================= */
let sliderValue = ref(0)
const isButtonShow = computed(() => {
  return sliderValue.value === 100
})

/* ================= 时钟 ================= */
const now = ref(new Date())
let timer = null

function updateTime() {
  now.value = new Date()
}
let currentYear = new Date().getFullYear()

const timeStr = computed(() => now.value.toLocaleTimeString('zh-CN', { hour12: false }))

const dateStr = computed(() => now.value.toLocaleDateString('zh-CN'))

/* ================= 打卡 ================= */
async function checkin() {
  sliderValue.value = 0
  try {
    const res = await api.post('/checkin')
    ElMessage.success(`打卡成功 🎉 第 ${res.data.rank} 名，获得 ${res.data.points_added} 积分`)
    await fetchPoints() // 打卡后刷新积分
  } catch (e) {
    ElMessage.warning(e.response?.data?.detail || '今日已打卡')
  }
}

/* ================= 退出 ================= */
async function logout() {
  try {
    await api.post('/logout')
    username.value = null
    myPoints.value = 0
    ElMessage.success('已退出登录')
  } catch {
    ElMessage.error('退出失败')
  }
}

/* ================= 今日排行榜 WS ================= */
const ranks = ref([])
let ws = null

function connectWS() {
  ws = new WebSocket(
    (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws/rank',
  )

  ws.onmessage = (e) => {
    ranks.value = JSON.parse(e.data)
  }

  ws.onclose = () => {
    setTimeout(connectWS, 2000)
  }
}

/* ================= 积分榜 ================= */
const pointsRank = ref([])

async function fetchPoints() {
  try {
    const res = await api.get('/points/rank')
    pointsRank.value = res.data

    if (username.value) {
      const me = res.data.find((u) => u.username === username.value)
      if (me) myPoints.value = me.points
    }
  } catch (e) {
    console.error(e)
  }
}

/* ================= 初始化 ================= */
onMounted(async () => {
  timer = setInterval(updateTime, 1000)

  try {
    const res = await api.get('/me')
    username.value = res.data.username
    myPoints.value = res.data.points
  } catch {
    username.value = null
  }

  connectWS()
  fetchPoints()
})

onUnmounted(() => {
  clearInterval(timer)
  ws?.close()
})
</script>

<template>
  <div class="container">
    <!-- 顶部用户栏 -->
    <el-card class="top-bar">
      <div v-if="loggedIn">
        👋 你好，<b>{{ username }}</b>
        <span class="points"> 当前积分：{{ myPoints }} </span>
        <el-button type="danger" size="small" @click="logout" style="margin-left: 12px">
          退出登录
        </el-button>
      </div>
      <div v-else>
        <el-button type="primary" @click="router.push('/login')"> 登录 / 注册 </el-button>
      </div>
    </el-card>

    <!-- 时钟 & 打卡 -->
    <el-card class="clock-card">
      <div class="date">{{ dateStr }}</div>
      <div class="time">{{ timeStr }}</div>
      <el-slider v-if="loggedIn" v-model="sliderValue" :show-tooltip="false" />
      <el-button
        v-if="loggedIn && isButtonShow"
        type="success"
        size="large"
        style="margin-top: 24px; width: 200px"
        @click="checkin"
      >
        今日打卡
      </el-button>

      <div v-else class="tip">登录并验证后才可以打卡</div>
    </el-card>

    <!-- 今日排行榜 -->
    <el-card class="rank-card">
      <h3>🏆 今日打卡排行榜</h3>

      <el-table :data="ranks" stripe style="margin-top: 12px">
        <el-table-column label="#" width="60">
          <template #default="scope">
            <span v-if="scope.$index === 0">🥇</span>
            <span v-else-if="scope.$index === 1">🥈</span>
            <span v-else-if="scope.$index === 2">🥉</span>
            <span v-else>{{ scope.$index + 1 }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="checkin_time" label="打卡时间" />
      </el-table>
    </el-card>

    <!-- 年度积分排行榜 -->
    <el-card class="rank-card">
      <h3>💎 年度积分排行榜</h3>

      <el-table :data="pointsRank" stripe style="margin-top: 12px">
        <el-table-column label="#" width="60">
          <template #default="scope">
            <span v-if="scope.$index === 0">🥇</span>
            <span v-else-if="scope.$index === 1">🥈</span>
            <span v-else-if="scope.$index === 2">🥉</span>
            <span v-else>{{ scope.$index + 1 }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="points" label="积分" />
      </el-table>
    </el-card>
    <el-footer style="text-align: center">
      © {{ currentYear }} <a href="https://github.com/yaoyangyaha">yaoyangyaha</a>
      <br />
      MIT license
    </el-footer>
  </div>
</template>

<style scoped>
.container {
  max-width: 720px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.points {
  margin-left: 20px;
  font-weight: bold;
  color: #409eff;
}

.clock-card {
  text-align: center;
  padding: 32px 0;
}

.date {
  font-size: 18px;
  color: #666;
}

.time {
  font-size: 48px;
  font-weight: bold;
  margin-top: 8px;
}

.tip {
  margin-top: 16px;
  color: #999;
}

.rank-card h3 {
  margin: 0;
}
</style>
