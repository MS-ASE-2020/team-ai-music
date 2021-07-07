<template>
    <el-container>
      <el-header>
        <vue-header></vue-header>
      </el-header>
      <el-main>
        <el-row type="flex" justify="center">
          <el-col :xs="24" :sm="24" :md="22" :lg="18" :xl="18" >
            <home-content></home-content>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
</template>

<script>
import VueHeader from '@/components/VueHeader.vue'
import HomeContent from '@/components/HomeContent.vue'

export default {
  name: 'Home',
  components: {
    VueHeader,
    HomeContent
  }
}
</script>

<style scoped>
.el-header {
  padding: 0 !important;
  border-bottom: 1px solid #eeeeee;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
