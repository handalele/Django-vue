<template>
  <div class="body">
    <div class="Box">
      <div class="left">
        <div class="centerBox">
          <img :src="logoUrl" alt="Logo" style="height: 120px;"/>
          <h4 style="color: white">CSDN</h4>
        </div>
      </div>

      <div class="right">
        <router-view></router-view>
      </div>
    </div>
  </div>

</template>
<script setup>

const logoUrl = new URL('@/assets/bc/logo.png', import.meta.url).href
</script>
<style>
.body {
  height: 100vh;
  background-color: aquamarine;
  background-image: url("@/assets/bc/background.jpg");
  background-size: cover;
}

.Box {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 55%;
  height: 60%;
  display: flex;
}

.left {
  position: relative;
  width: 50%;
  height: 100%;
  background-color: rgba(57, 99, 134, 0.75);
}

.right {
  position: relative;
  width: 50%;
  height: 100%;
  background-color: rgba(255, 255, 255, 1);
}

.centerBox {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  text-align: center;
}
</style>