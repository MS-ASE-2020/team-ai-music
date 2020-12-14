<template>
    <div>
        <el-card>
            <div class='list'>
                <el-row v-for="(data, index) in tableData" :key="index" :gutter="20">
                    <el-card class="card-h" shadow="hover" >
                        <el-col :span="4">
                            <div>
                                <span>{{ data.name }}</span>
                            </div>
                        </el-col>
                        <el-col :span="10">
                            <div>
                                <span>{{ data.gen_date }}</span>
                            </div>
                        </el-col>
                        <el-col :span="4">
                            <el-button @click="del(data.music_id)" size="small">删除</el-button>
                        </el-col>
                    </el-card>
                </el-row>
            </div>
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
        url: 'http://127.0.0.1:8000/music/get/',
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
        url: `http://127.0.0.1:8000/music/delete/${id}`,
        method: 'GET'
      }).then(function (ret) {
        console.log(ret)
        vm.getList()
      })
      this.$message.success('delete successfully!')
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
    margin-bottom: 5px;
}
</style>
