<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "../api"

const router = useRouter()
const user = ref(null)
const ranks = ref([])

onMounted(async () => {
  try {
    user.value = (await api.get("/me")).data
  } catch {
    user.value = null
  }

  const ws = new WebSocket("ws://localhost:8000/ws/rank")
  ws.onmessage = e => ranks.value = JSON.parse(e.data)
})
</script>

<template>
  <el-card>
    <div v-if="user">
      👋 欢迎，<b>{{ user.username }}</b>
      <el-button type="success" @click="$router.push('/checkin')">
        打卡
      </el-button>
    </div>

    <div v-else>
      <el-button type="primary" @click="router.push('/login')">
        登录
      </el-button>
    </div>

    <el-divider />

    <el-table :data="ranks">
      <el-table-column prop="rank" label="排名" />
      <el-table-column prop="username" label="用户" />
      <el-table-column prop="time" label="时间" />
    </el-table>
  </el-card>
</template>
