<template>
    <div>
        <el-card>
            <div class='lyrics'>
                <span class='hint'>请输入歌词：</span>
                <el-input
                    type="textarea"
                    :rows="10"
                    placeholder="请输入歌词"
                    v-model="textarea">
                </el-input>
            </div>
            <div>
                <el-select v-model="emotion" placeholder="请选择情绪">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
                <el-button @click="submit">生成</el-button>
            </div>
            <div>
                <aplayer :music="{
                    title: 'Sample',
                    author: 'PopMag',
                    url: 'https://speechresearch.github.io/popmag/audio/2_gt.mp3',
                    pic: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=467066316,1812256104&fm=26&gp=0.jpg',
                    lrc: '[00:00.00]lrc here\n[00:01.00]aplayer\n[01:00.00]lyric'
                    }" :showLrc=true :theme='pic'>
                    </aplayer>
            </div>
            <div>
                <el-button @click="share">分享</el-button>
                <el-button @click="save">保存</el-button>
            </div>
        </el-card>
    </div>
</template>

<script>
import Aplayer from 'vue-aplayer'
export default {
  name: 'HomeContent',
  data () {
    return {
      textarea: '',
      options: [{
        value: 'happy',
        label: '愉悦'
      }, {
        value: 'sad',
        label: '悲伤'
      }, {
        value: 'angry',
        label: '愤怒'
      }],
      emotion: ''
    }
  },
  components: {
    Aplayer
  },
  methods: {
    submit () {
      if ((this.textarea === '') | (this.emotion === '')) {
        this.$message.info('Please input the lyrics and select the emotion!')
      } else {
        this.$message.success('Submit succesfully!')
        console.log(this.textarea)
        console.log(this.emotion)
        console.log('submit')
        // this.$axios.request({
        //   url: 'http://127.0.0.1:8000/music/get',
        //   method: 'GET'
        // }).then(function (ret) {
        //   console.log(ret)
        //   if (ret.data.status === 0) {
        //     this.tableData = ret.data
        //   }
        // })
      }
    },
    share () {
      console.log('share')
    },
    save () {
      console.log('save')
    }
  }
}
</script>

<style scoped>
.lyrics {
  display: flex;
  flex-direction: row;
  height: 200px;
  align-items: center;
}
div {
  margin-top:20px;
}

</style>
