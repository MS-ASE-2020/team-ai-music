<template>
    <el-row class="header" type="flex" justify="space-between">
    <el-col :span="4">
      <div class="center">
        <!-- In Vue tmplate, import an image is tricky， we use webpack require syntax here -->
        <div class="logo-img">
            <el-avatar class="profile-photo"
            src="/static/icons/logo.jpg"></el-avatar>
        </div>
        <div>AI-MUSIC</div>
      </div>
    </el-col>
    <el-col>
        <div class="nav-bar">
            <el-menu mode="horizontal">
            <el-menu-item><a href="#/home">主页</a></el-menu-item>
            <el-menu-item><a href="#/history">历史</a></el-menu-item>
            </el-menu>
        </div>
    </el-col>
    <el-col :span="2">
      <div class="center" >
        <el-dropdown placement="bottom" @command="commandHandler" size="medium">
          <el-avatar class="profile-photo"
            src="/static/icons/user.jpg"></el-avatar>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item :command="login">登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-col>
    <el-dialog title="login" :visible.sync="dialogVisible" width="300px">
        <el-form :model="form" status-icon :rules="rules" rel="form">
          <el-form-item label="username" :label-width="formLabelWidth" prop="name">
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="password" :label-width="formLabelWidth" prop="password">
            <el-input v-model="form.password" autocomplete="off" show-password></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="userlogin">确 定</el-button>
        </div>
      </el-dialog>

  </el-row>
</template>

<script>

export default {
  name: 'VueHeader',
  data () {
    // var validate = (rule, value, callback) => {
    //   callback()
    // }
    return {
      dialogVisible: false,
      form: {
        name: '',
        password: ''
      },
      rules: {
        name: [
          { required: true }
        ],
        password: [
          { required: true, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    commandHandler (command) {
      this.dialogVisible = true
    },
    userlogin () {
      var vm = this
      console.log('login')
      // this.$message.success('log in!')
      this.$axios.request({
        url: 'http://127.0.0.1:9000/login/',
        method: 'POST',
        data: 'form'
      }).then(function (ret) {
        console.log(ret)
        if (ret.status === 500) {
          vm.$message.fail('log in fail')
        } else if (ret.status === 200) {
          vm.$message.success('login success')
        }
      })
      // this.dialogVisible = true
      // this.SuccessVisible = true
    }
    // loginFinish () {
    //   // console.log('login')
    //   // this.dialogVisible = false
    //   this.SuccessVisible = false
    // }
  }
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
