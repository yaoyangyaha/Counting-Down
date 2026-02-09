<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const username = ref(null)
const loggedIn = computed(() => !!username.value)

const now = ref(new Date())
let timer = null

function updateTime() {
  now.value = new Date()
}

const timeStr = computed(() => now.value.toLocaleTimeString('zh-CN', { hour12: false }))

const dateStr = computed(() => now.value.toLocaleDateString('zh-CN'))

async function checkin() {
  try {
    await api.post('/checkin')
    ElMessage.success('打卡成功 🎉')
  } catch (e) {
    ElMessage.warning(e.response?.data?.detail || '今日已打卡')
  }
}

async function logout() {
  try {
    await api.post('/logout')
    username.value = null // 更新前端状态
    ElMessage.success('已退出登录')
  } catch (e) {
    ElMessage.error('退出失败')
  }
}

const ranks = ref([])
let ws = null

function connectWS() {
  ws = new WebSocket('ws://localhost:8000/ws/rank')

  ws.onmessage = (e) => {
    ranks.value = JSON.parse(e.data)
  }

  ws.onclose = () => {
    // 简单重连
    setTimeout(connectWS, 2000)
  }
}

onMounted(async () => {
  // 时钟
  timer = setInterval(updateTime, 1000)

  // 登录态
  try {
    const res = await api.get('/me')
    username.value = res.data.username
  } catch {
    username.value = null
  }

  // WS
  connectWS()
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

      <el-button
        v-if="loggedIn"
        type="success"
        size="large"
        style="margin-top: 24px; width: 200px"
        @click="checkin"
      >
        今日打卡
      </el-button>

      <div v-else class="tip">登录后才可以打卡</div>
    </el-card>

    <!-- 排行榜 -->
    <el-card class="rank-card">
      <h3>🏆 今日打卡排行榜</h3>

      <el-table :data="ranks" stripe style="margin-top: 12px">
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="time" label="打卡时间" />
      </el-table>
    </el-card>
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
