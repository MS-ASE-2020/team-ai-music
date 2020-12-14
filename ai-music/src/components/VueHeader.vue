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
            <el-dropdown-item command="login">登录</el-dropdown-item>
            <el-dropdown-item command="register">注册</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-col>
    <el-dialog title='register' :visible.sync="registerdialog" width="300px">
        <el-form :model="registerform" :rules="registerrules" rel="form">
          <el-form-item label="username" :label-width="formLabelWidth" prop="username">
            <el-input v-model="registerform.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="password" :label-width="formLabelWidth" prop="password">
            <el-input v-model="registerform.password" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item label="comfirm password" :label-width="formLabelWidth" prop="checkpassword">
            <el-input v-model="registerform.checkpassword" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-button type="primary" @click="userregister('registerform')">确 定</el-button>
        </el-form>
      </el-dialog>
    <el-dialog title="login" :visible.sync="logindialog" width="300px">
        <el-form :model="form" status-icon :rules="rules" rel="form">
          <el-form-item label="username" :label-width="formLabelWidth" prop="name">
            <el-input v-model="form.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="password" :label-width="formLabelWidth" prop="password">
            <el-input v-model="form.password" autocomplete="off" show-password></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="logindialog = false">取 消</el-button>
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
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password'))
      } else {
        if (this.registerform.checkpassword !== '') {
          this.$refs.registerform.validateField('checkpassword')
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
        name: [
          { required: true }
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
  methods: {
    commandHandler (command) {
      if (command === 'login') {
        this.logindialog = true
      } else if (command === 'register') {
        this.registerdialog = true
      }
    },
    userlogin () {
      var vm = this
      console.log('login')
      // this.$message.success('log in!')
      this.$axios.request({
        url: 'http://127.0.0.1:9000/login/',
        method: 'POST',
        data: vm.form
      }).then(function (ret) {
        console.log(ret)
        if (ret.status === 500) {
          vm.$message.error('log in fail')
        } else if (ret.status === 200) {
          vm.$message.success('login success')
        }
      })
      // this.dialogVisible = true
      // this.SuccessVisible = true
    },
    userregister (formName) {
      this.$message.success(formName)
      this.registerform.resetFields()
      this.registerform.validate((valid) => {
        this.$message.success(valid)
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
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
