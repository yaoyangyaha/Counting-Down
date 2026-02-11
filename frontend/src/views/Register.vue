<script setup>
import { ref } from 'vue'
import api from '../api'
import { ElMessage } from 'element-plus'

const form = ref({
  username: '',
  password: '',
})

const passwordRetype = ref('')

function toLogin() {
  window.location.href = '/login'
}

async function register() {
  try {
    if (passwordRetype.value !== form.value.password) {
      ElMessage.error('两次密码不一致')
      return
    } else if (passwordRetype.value.length < 6) {
      ElMessage.error('密码过短')
      return
    }
    await api.post('/register', {
      username: form.value.username,
      password: form.value.password,
    })

    ElMessage.success('注册成功，请登录')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '注册失败')
  }
}
</script>

<template>
  <el-card class="box">
    <h2>注册</h2>

    <el-input v-model="form.username" placeholder="用户名" />
    <el-input
      v-model="form.password"
      type="password"
      placeholder="密码"
      show-password
      style="margin-top: 12px"
      minlength="6"
      maxlength="20"
    />

    <el-input
      v-model="passwordRetype"
      type="password"
      placeholder="再次输入密码"
      show-password
      style="margin-top: 12px"
      minlength="6"
      maxlength="20"
    />

    <el-button type="primary" style="margin-top: 16px; width: 100%" @click="register">
      注册
    </el-button>

    <el-link style="margin-top: 12px" @click="toLogin()"> 已有账号？去登录 </el-link>
  </el-card>
</template>

<style scoped>
.box {
  width: 360px;
  margin: 120px auto;
}
</style>
