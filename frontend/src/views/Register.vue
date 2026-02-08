<script setup>
import { ref } from "vue"
import api from "../api"
import { ElMessage } from "element-plus"

const form = ref({
  username: "",
  password: ""
})

const emit = defineEmits(["to-login"])

async function register() {
  try {
    await api.post("/register", null, { params: form.value })
    ElMessage.success("注册成功，请登录")
    emit("to-login")
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || "注册失败")
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
        style="margin-top:12px"
    />

    <el-button type="primary" style="margin-top:16px;width:100%" @click="register">
      注册
    </el-button>

    <el-link style="margin-top:12px" @click="emit('to-login')">
      已有账号？去登录
    </el-link>
  </el-card>
</template>

<style scoped>
.box {
  width: 360px;
  margin: 120px auto;
}
</style>
