<template>
    <el-row>
      <el-col>
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
                <el-select v-model="instruments" multiple placeholder="请选择乐器">
                  <el-option
                    v-for="item in options_instru"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
                <el-button @click="reset" style="margin-left: 10px">重置</el-button>
                <el-button @click="submit">生成</el-button>
            </div>
            <el-image src="static/line.jpg" style="width: 20%"></el-image>
            <el-image src="static/line.jpg" style="width: 20%; margin-left: 50px"></el-image>
            <div>
                <aplayer :music="{
                    title: 'Sample',
                    artist: 'PopMag',
                    src: music_url,
                    pic: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=467066316,1812256104&fm=26&gp=0.jpg',
                    lrc: '[00:00.00]lrc1\n[00:01.00]lrc2\n[00:02:00]lrc3\n[00:03.00]lyc4'
                    }" :showLrc=true :theme='pic'>
                    </aplayer>
            </div>
            <div>
                <el-button @click="share">保存并分享</el-button>
                <el-button @click="save_btn">保存</el-button>
            </div>
        </el-card>
      </el-col>
      <el-dialog title="save" :visible.sync="dialogVisible" width="300px">
        <el-form :model="form">
          <el-form-item label="music name">
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="save">确 定</el-button>
        </div>
      </el-dialog>
      <el-dialog title="share" :visible.sync="GenMusicDialogVisible" width="300px">
        <el-progress :text-inside="true" :stroke-width="26" :percentage="percentage"></el-progress>
        <div slot="footer" class="dialog-footer">
          <el-button @click="shareDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="save">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="share" :visible.sync="shareDialogVisible" width="300px">
        <el-form :model="share">
          <el-form-item label="music name">
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <el-button @click="save_share">生成分享链接</el-button>
        <div>
          <el-input v-model="share_url">
            <el-button slot="append" icon="el-icon-document-copy" @click="copy"
              :data-clipboard-text="share_url" class="copyBtn"></el-button>
          </el-input>
        </div>
        <div slot="footer" class="dialog-footer">
          <el-button @click="shareDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="save">确 定</el-button>
        </div>
      </el-dialog>
    </el-row>
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
      options_instru: [{
        value: 'Piano',
        label: 'Piano'
      }, {
        value: 'Guitar',
        label: 'Guitar'
      }, {
        value: 'Bass',
        label: 'Bass'
      }, {
        value: 'Strings',
        label: 'Strings'
      }, {
        value: 'Drums',
        label: 'Drums'
      }, {
        value: 'Lead',
        label: 'Lead'
      }],
      instruments: [],
      emotion: '',
      music_id: '',
      music_url: '',
      dialogVisible: false,
      shareDialogVisible: false,
      GenMusicDialogVisible: false,
      share_url: '',
      form: {
        name: ''
      },
      persentage: 0,
      status: 0,
      ret_id: 0
    }
  },
  components: {
    Aplayer
  },
  mounted: function () {
    console.log(this.$route)
    console.log(this.$route.query.music_id)
    var vm = this
    if (this.$route.query.music_id) {
      this.music_id = this.$route.query.music_id
      this.$axios.request({
        url: `http://127.0.0.1:9000/music/info/${this.music_id}`,
        method: 'GET'
      }).then(function (ret) {
        console.log(ret)
        if (ret.status === 200) {
          vm.textarea = ret.data.text
          vm.instruments = ret.data.instruments
          vm.emotion = ret.data.emotion
          vm.music_url = `http://127.0.0.1:9000/download/${vm.music_id}.mp3`
        }
      })
    }
  },
  methods: {
    copy () {
      console.log('copy')
      var vm = this
      var clipboard = new this.Clipboard('.copyBtn')
      clipboard.on('success', function () {
        console.log('copy success')
        vm.$message.success('Copy successfully!')
      })
      clipboard.on('error', function () {
        console.log('copy error')
      })
    },
    reset () {
      if (this.$route.fullPath !== '/home') {
        this.$router.push({
          path: `/home`,
          name: 'Home',
          replace: true
        })
      }
      this.$router.go(0)
    },
    submit () {
      var vm = this
      if ((this.textarea === '') | (this.emotion === '')) {
        this.$message.info('Please input the lyrics and select the emotion!')
      } else {
        this.$message.success('Submit succesfully! Please wait for your music...')
        console.log(this.textarea)
        console.log(this.emotion)
        console.log('submit')
        var data = {'text': vm.textarea, 'emotion': vm.emotion, 'instruments': vm.instruments}
        this.$axios.post('http://127.0.0.1:9000/generate/', data)
          .then(function (ret) {
            console.log(ret)
            if (ret.status === 200) {
              console.log('submit successfully!')
              vm.ret_id = ret.id
              vm.GenMusicDialogVisible = true
              do {
                this.$axios.request({
                  url: `http://127.0.0.1:9000/music/status/${vm.ret_id}/`,
                  method: 'GET'
                }).then(function (ret) {
                  console.log(ret)
                  vm.status = ret
                  console.log(ret)
                })
              }
              while (vm.status < 3)
            }
          })
      }
    },
    share () {
      console.log('share')
      this.shareDialogVisible = true
      this.$message.success('Share successfully!')
    },
    save_share () {
      this.save()
      console.log(this.$route)
      this.share_url = 'http://127.0.0.1:8080/?#' + this.$route.path + '?' + this.music_id
    },
    save_btn () {
      console.log('save')
      this.dialogVisible = true
    },
    save () {
      var vm = this
      vm.dialogVisible = false
      console.log('save with name')
      var data = {'id': vm.music_id, 'name': vm.form.name}
      this.$axios.post('http://127.0.0.1:9000/save/', data)
        .then(function (ret) {
          console.log(ret)
          if (ret.status === 200) {
            vm.$message.success('Save successfully!')
          }
        })
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
.hint {
  width: 120px;
}
.el-image {
  margin-top: 30px;
  margin-bottom: 10px;
}
</style>
