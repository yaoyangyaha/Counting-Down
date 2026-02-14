<script setup>
import { ref } from 'vue'
import api from '../api'
import { ElLink, ElMessage } from 'element-plus'
import VueTurnstile from 'vue-turnstile'
function toRegister() {
  window.location.href = '/register'
}

const username = ref('')
const password = ref('')
const turnstileToken = ref('')

async function login() {
  try {
    const res = await api.post('/login', {
      username: username.value,
      password: password.value,
      turnstile_token: turnstileToken.value,
    })

    localStorage.setItem('token', res.data.token)
    localStorage.setItem('username', res.data.username)

    ElMessage.success('登录成功')
    window.location.href = '/'
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '账号或密码错误')
    turnstileToken.value = ''
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
    <VueTurnstile site-key="1x00000000000000000000AA" v-model="turnstileToken" />

    <el-button type="primary" :disabled="!turnstileToken" @click="login"> 登录 </el-button>

    <el-link @click="toRegister()"> 没有账号？去注册 </el-link>
  </el-card>
</template>

<style scoped>
.box {
  width: 360px;
  margin: 120px auto;
}
</style>
