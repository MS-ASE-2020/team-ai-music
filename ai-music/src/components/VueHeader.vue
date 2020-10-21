<template>
    <el-row class="header" type="flex" justify="space-between">
    <el-col :span="4">
      <div class="center">
        <!-- In Vue tmplate, import an image is tricky， we use webpack require syntax here -->
        <div class="logo-img">
            <el-avatar class="profile-photo"
            src="https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=467066316,1812256104&fm=26&gp=0.jpg"></el-avatar>
        </div>
        <div>AI-MUSIC</div>
      </div>
    </el-col>
    <el-col>
        <div class="nav-bar">
            <el-menu mode="horizontal">
            <el-menu-item><a>主页</a></el-menu-item>
            <el-menu-item><a>历史</a></el-menu-item>
            </el-menu>
        </div>
    </el-col>
    <el-col :span="2">
      <div class="center" >
        <el-dropdown placement="bottom" @command="commandHandler" size="medium">
          <el-avatar class="profile-photo"
            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile">个人资料</el-dropdown-item>
            <el-dropdown-item command="logout">登出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-col>
  </el-row>
</template>

<script>

export default {
  name: 'VueHeader'
}
</script>

<style scoped>
.header {
  height: 100%;
}
.center {
  height: 100%;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
.logo-img {
  height: 40px;
  width: 40px;
  background-size: contain;
  background-repeat: no-repeat;
  margin-right: 20px;
}
.profile-photo {
  cursor: pointer;
}
.el-menu {
  display: flex;
  justify-content: flex-start;
}
a {
  text-decoration: none;
}
</style>
