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
            <el-dropdown-item command="login" v-show="log_status === false">登录</el-dropdown-item>
            <el-dropdown-item command="register" v-show="log_status === false">注册</el-dropdown-item>
            <el-dropdown-item command="logout" v-show="log_status === true">登出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-col>
    <el-dialog title='register' :visible.sync="registerdialog" width="300px">
        <el-form :model="registerform" :rules="registerrules" ref="registerform">
          <el-form-item label="username" prop="username">
            <el-input v-model="registerform.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="password" prop="password">
            <el-input v-model="registerform.password" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item label="comfirm password" prop="checkpassword">
            <el-input v-model="registerform.checkpassword" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-button @click="registerdialog = false">取 消</el-button>
          <el-button type="info" @click="$refs['registerform'].resetFields()">重 置</el-button>
          <el-button type="primary" @click="userregister('registerform')">确 定</el-button>
        </el-form>
      </el-dialog>
    <el-dialog title="login" :visible.sync="logindialog" width="300px">
        <el-form :model="form" status-icon :rules="rules" ref="form">
          <el-form-item label="username" prop="username">
            <el-input v-model="form.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="password" prop="password">
            <el-input v-model="form.password" autocomplete="off" show-password></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="logindialog = false">取 消</el-button>
          <el-button type="info" @click="$refs['form'].resetFields()">重 置</el-button>
          <el-button type="primary" @click="userlogin">确 定</el-button>
        </div>
      </el-dialog>

  </el-row>
</template>

<script>

export default {
  name: 'VueHeader',
  data () {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password'))
      } else {
        if (this.registerform.checkpassword !== '') {
          this.$refs['registerform'].validateField('checkpassword')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password again'))
      } else if (value !== this.registerform.password) {
        callback(new Error('Two inputs don\'t match!'))
      } else {
        callback()
      }
    }
    return {
      logindialog: false,
      registerdialog: false,
      log_status: false,
      form: {
        username: '',
        password: ''
      },
      registerform: {
        username: '',
        password: '',
        checkpassword: ''
      },
      rules: {
        username: [
          { required: true, trigger: 'blur' }
        ],
        password: [
          { required: true, trigger: 'blur' }
        ]
      },
      registerrules: {
        username: [
          { required: true }
        ],
        password: [
          { validator: validatePass, required: true, trigger: 'blur' }
        ],
        checkpassword: [
          { validator: validatePass2, required: true, trigger: 'blur' }
        ]
      }
    }
  },
  created: function () {
    this.is_auth()
  },
  methods: {
    is_auth () {
      console.log('is_auth')
      var vm = this
      this.$axios.request({
        url: 'http://127.0.0.1:9000/is_auth/',
        method: 'GET'
      }).then(function (ret) {
        console.log(ret)
        if (ret.data === 'False') {
          vm.log_status = false
        } else {
          vm.log_status = true
        }
      })
    },
    commandHandler (command) {
      if (command === 'login') {
        this.logindialog = true
      } else if (command === 'register') {
        this.registerdialog = true
      } else if (command === 'logout') {
        console.log('logout')
        var vm = this
        this.$axios.request({
          url: 'http://127.0.0.1:9000/logout/',
          method: 'GET'
        }).then(function (ret) {
          console.log(ret)
          vm.is_auth()
        })
      }
    },
    userlogin () {
      var vm = this
      console.log('login')
      console.log(vm.form)
      this.$axios.request({
        url: 'http://127.0.0.1:9000/login/',
        method: 'POST',
        data: vm.form
      }).then(function (ret) {
        console.log(ret)
        if (ret.status === 200) {
          vm.$message.success('Login success!')
          vm.logindialog = false
          vm.$refs['form'].resetFields()
          vm.is_auth()
        } else {
          vm.$message.error('Login fail! Please check your username and password!')
        }
      })
    },
    userregister (formName) {
      var vm = this
      console.log(formName)
      console.log(this.registerform)
      vm.$refs[formName].validate((valid) => {
        console.log(valid)
        if (valid) {
          var regForm = {
            username: vm.registerform.username,
            password: vm.registerform.password
          }
          this.$axios.request({
            url: 'http://127.0.0.1:9000/register/',
            method: 'POST',
            data: regForm
          }).then(function (ret) {
            console.log(ret)
            if (ret.status === 200) {
              vm.$message.success('Regitster submit successfully! Please login!')
            } else {
              console.log('register fail')
            }
          })
        } else {
          console.log('Do not follow the rules')
          return false
        }
      })
      // vm.$refs[formName].resetFields()
    }
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
