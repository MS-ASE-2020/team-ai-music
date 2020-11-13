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
                        <el-col :span="4">
                            <div>
                                <span>{{ data.date }}</span>
                            </div>
                        </el-col>
                        <el-col :span="6">
                            <el-button size="small">删除</el-button>
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
      tableData: [{
        id: '1',
        date: '2016-05-02',
        name: 'music1'
      }, {
        id: '2',
        date: '2016-05-04',
        name: 'music2'
      }, {
        id: '3',
        date: '2016-05-01',
        name: 'music3'
      }, {
        id: '4',
        date: '2016-05-03',
        name: 'music4'
      }]
    }
  },
  mounted: function () {
    this.getList()
  },
  methods: {
    getList: function () {
      this.$axios.request({
        url: 'http://127.0.0.1:8000/music/get/',
        method: 'GET'
      }).then(function (ret) {
        console.log(ret)
        if (ret.data.status === 0) {
          this.tableData = ret.data
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
    margin-bottom: 5px;
}
</style>
