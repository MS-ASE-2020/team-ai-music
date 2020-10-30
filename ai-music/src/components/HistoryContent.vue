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
        date: '2016-05-02',
        name: 'music1'
      }, {
        date: '2016-05-04',
        name: 'music2'
      }, {
        date: '2016-05-01',
        name: 'music3'
      }, {
        date: '2016-05-03',
        name: 'music4'
      }]
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
