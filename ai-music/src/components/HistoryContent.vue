<template>
    <div>
        <el-card>
          <el-col :span="12">
            <div class='list'>
                <el-row v-for="(data, index) in tableData" :key="index" :gutter="20" :justify="center" :align="middle">
                    <el-card class="card-h" shadow="hover" >
                        <el-col :span="4">
                            <div class="card-text">
                                <span>{{ data.name }}</span>
                            </div>
                        </el-col>
                        <el-col :span="10">
                            <div class="card-text">
                                <span>{{ data.gen_date }}</span>
                            </div>
                        </el-col>
                        <el-col :span="5" :offset="4.5">
                            <div>
                              <el-button @click="del(data.music_id)" size="small" icon="el-icon-delete"></el-button>
                            </div>
                        </el-col>
                        <el-col :span="0.5">
                            <div>
                              <el-button @click="detail(data.music_id)" size="small" icon="el-icon-edit-outline"></el-button>
                            </div>
                        </el-col>
                    </el-card>
                </el-row>
            </div>
          </el-col>
          <el-col :span="10">
            <el-image src="/static/history_bg.jpg" class="img-bg"></el-image>
          </el-col>
        </el-card>
    </div>
</template>

<script>
export default {
  name: 'HistoryContent',
  data () {
    return {
      tableData: []
    }
  },
  mounted: function () {
    this.getList()
  },
  methods: {
    getList: function () {
      var vm = this
      this.$axios.request({
        url: 'http://127.0.0.1:9000/music/get/',
        method: 'GET'
      }).then(function (ret) {
        console.log(ret)
        if (ret.status === 200) {
          vm.tableData = ret.data
          console.log(vm.tableData)
        }
      })
    },
    del: function (id) {
      console.log('delete')
      console.log(id)
      var vm = this
      this.$axios.request({
        url: `http://127.0.0.1:9000/music/delete/${id}`,
        method: 'GET'
      }).then(function (ret) {
        console.log(ret)
        vm.getList()
      })
      this.$message.success('delete successfully!')
    },
    detail: function (id) {
      console.log('detail')
      console.log(id)
      this.$router.push({
        path: `/home`,
        name: 'Home',
        query: {
          music_id: id
        }
      })
    }
  }
}
</script>

<style scoped>
.list {
  margin-top: 20px;
}
.el-card {
  margin-bottom: 20px;
}
.card-h {
  background: #F0F8FF;
}
.el-button {
    margin-bottom: 00px;
    text-align: right;
}
.img-bg {
  margin-bottom: 10px;
}
.card-text {
  margin-bottom: 10px;
}
</style>
