<script setup>
import { ref } from 'vue'
import api from '../api'
import { ElLink, ElMessage } from 'element-plus'

function toRegister() {
  window.location.href = '/register'
}

const username = ref('')
const password = ref('')

async function login() {
  try {
    const res = await api.post('/login', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('token', res.data.token)
    localStorage.setItem('username', res.data.username)

    ElMessage.success('登录成功')
    window.location.href = '/'
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '账号或密码错误')
  }
}
</script>

<template>
  <el-card class="box">
    <h2>登录</h2>

    <el-input v-model="username" placeholder="用户名" />
    <el-input
      v-model="password"
      type="password"
      placeholder="密码"
      show-password
      style="margin-top: 12px"
    />

    <el-button type="primary" style="margin-top: 16px; width: 100%" @click="login">
      登录
    </el-button>

    <el-link @click="toRegister()"> 没有账号？去注册 </el-link>
  </el-card>
</template>

<style scoped>
.box {
  width: 360px;
  margin: 120px auto;
}
</style>
