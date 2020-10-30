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
                <el-select v-model="value" placeholder="请选择情绪">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
                <el-button>生成</el-button>
            </div>
            <div>
                <aplayer autoplay :music="{
                    title: 'Sample',
                    author: 'PopMag',
                    url: 'https://speechresearch.github.io/popmag/audio/2_gt.mp3',
                    pic: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=467066316,1812256104&fm=26&gp=0.jpg',
                    lrc: '[00:00.00]lrc here\n[00:01.00]aplayer\n[01:00.00]lyric'
                    }" :showLrc=true :theme='pic'>
                    </aplayer>
            </div>
            <div>
                <el-button>分享</el-button>
                <el-button>保存</el-button>
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
      value: ''
    }
  },
  components: {
    Aplayer
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
