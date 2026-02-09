<script setup>
import { ref } from "vue"
import api from "../api"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"

const router = useRouter()
const form = ref({ username: "", password: "" })

async function login() {
  try {
    await api.post("/login", form.value)
    ElMessage.success("登录成功")
    await router.push("/")
  } catch {
    ElMessage.error("登录失败")
  }
}
</script>

<template>
  <el-card class="box">
    <h2>登录</h2>

    <el-input v-model="form.username" placeholder="用户名" />
    <el-input
        v-model="form.password"
        type="password"
        placeholder="密码"
        show-password
        style="margin-top:12px"
    />

    <el-button type="primary" style="margin-top:16px;width:100%" @click="login">
      登录
    </el-button>

    <el-link style="margin-top:12px" @click="emit('to-register')">
      没有账号？去注册
    </el-link>
  </el-card>
</template>

<style scoped>
.box {
  width: 360px;
  margin: 120px auto;
}
</style>
