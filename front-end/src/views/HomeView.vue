<script setup lang="ts">
import {reactive, ref} from 'vue'
import {useDark, useToggle} from '@vueuse/core'
import {ElLoading, ElMessage} from 'element-plus'
import AdvancedSettingDlg from '@/views/components/AdvancedSettingDlg.vue'
import SearchResultList from '@/views/components/SearchResultList.vue'
import {documentSearch, guessYourLike} from '@/helper/api/document.js'
import AutoComplete from "@/views/components/AutoComplete.vue";
import LogoComponent from "@/views/components/LogoComponent.vue";


// First entry
let firstEntry = ref(true)
// Query content
let searchContent = reactive({
  query: '',
  searchtype: 'title',
  year: '',
  sp_year: '',
  sp_author: '',
  confs: [
    'AAAI',
    'ACL',
    'AISTATS',
    'BMVC',
    'CIKM',
    'COLING',
    'COLT',
    'CVPR',
    'ECCV',
    'ECIR',
    'EMNLP',
    'FAST',
    'ICASSP',
    'ICCV',
    'ICDM',
    'ICLR',
    'ICME',
    'ICML',
    'IJCAI',
    'IJCV',
    'INTERSPEECH',
    'ISWC',
    'JMLR',
    'KDD',
    'MICCAI',
    'MLSYS',
    'MM',
    'NAACL',
    'NIPS',
    'RECSYS',
    'SIGIR',
    'SIGMOD',
    'TASLP',
    'TIP',
    'TKDE',
    'TNNLS',
    'TOIS',
    'TPAMI',
    'VLDB',
    'WACV',
    'WSDM',
    'WWW'
  ]
})

// Query result
let queryResult = reactive({
  val: {}
})
// Advanced setting dialog
const settingDlg = ref(null)
// Search result component
const searchResult = ref(null)

// Handle Search
let guessLoading = ref(false)
let guessList = reactive({
  val: []
})
const search = (): void => {
  if (searchContent.query === '' && searchContent.sp_author === '') {
    ElMessage.warning('Please input your keywords for search.')
    return
  }
  const loading = ElLoading.service({
    lock: true,
    text: 'Searching...'
    // background: 'rgba(0, 0, 0, 0.7)',
  })
  queryResult.val = {}
  guessList.val = []
  documentSearch({
    ...searchContent,
    confs: searchContent.confs.join(',')
  })
      .then((res: any) => {
        const {data, msg} = res
        if (msg === 'success') {
          queryResult.val = data
          handleTreeClick({level: 1})
        }
      })
      .catch(err => {
        console.log(err)
      })
      .finally(() => {
        firstEntry.value = false
        loading && loading.close()
      })
  guessLoading.value = true
  guessYourLike({query: searchContent.query})
      .then((res: any) => {
        const {data, msg} = res
        if (msg === 'success' && data.keywords) {
          guessList.val = data.keywords
        }
      })
      .catch(err => {
        console.log(err)
      })
      .finally(() => {
        guessLoading.value = false
      })
}

// Handle search author
const handleSearchAuthor = (data: string): void => {
  searchContent.query = ''
  // searchContent.searchtype = 'author'
  searchContent.sp_author = data
  search()
}


// Handle tree click
const handleTreeClick = (data: Object): void => {
  if (searchResult.value) {
    ;(searchResult.value as any).filterResult(queryResult.val, data)
  }
}

// Show advanced setting dialog
const showSetting = (): void => {
  if (settingDlg.value) {
    ;(settingDlg.value as any).isVisible = true
  }
}

// Change dark mode
const isDark = useDark()
const toggleDark = useToggle(isDark)

</script>

<template>
  <main class="full pos-relative">
    <!-- Theme Mode -->
    <div class="mb-15 mt-15 mr-15" style="text-align: end;">
      <el-link type="primary" :icon="isDark ? 'Sunny' : 'Moon'" @click="toggleDark()">
      </el-link>
    </div>
    <el-row justify="center" :class="['mb-15 pos-absolute', firstEntry ? 'first-entry' : 'normal']">
      <el-col class="gutter-20" :xs="24" :sm="16" :md="14" :lg="10" :xl="8">
        <el-row align="middle" style="justify-content: center;">
          <!-- Title -->
          <LogoComponent v-show="firstEntry"></LogoComponent>
          <h1 class="title mb-15" v-show="firstEntry"><a href="/">IR Engine</a></h1>
          <el-col :span="6" v-show="!firstEntry">
            <LogoComponent v-show="!firstEntry"></LogoComponent>
            <!--            <h4 class="title mb-15" style="font-size: 20px !important;"><a href="/">IR Engine</a></h4>-->
          </el-col>
          <!-- Search Bar -->
          <el-col :span="18">
            <AutoComplete @search="search" v-model:search-content="searchContent"></AutoComplete>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <el-row justify="center" v-show="!firstEntry">
      <el-col class="gutter-20" :xs="24" :sm="16" :md="14" :lg="10" :xl="8">
        <!-- Search result list -->
        <SearchResultList ref="searchResult" @search-author="handleSearchAuthor"/>
      </el-col>
    </el-row>
    <!-- Advanced setting dialog -->
    <AdvancedSettingDlg ref="settingDlg" v-model:data="searchContent"/>
    <!-- Back to top -->
    <el-backtop :right="50" :bottom="50"/>
  </main>
</template>

<style scoped>
.title {
  font-size: 60px;
  text-align: center;
  user-select: none;
}

.title a {
  text-decoration: none;
  color: #333;
}

.title a:hover {
  text-decoration: underline;
}

.toolbar {
  text-align: center;
  user-select: none;
}

.toolbar a + a {
  margin-left: 20px;
}

.gutter-20 {
  padding: 0 20px;
}

.first-entry {
  top: calc(50% - 80px);
  transform: translateY(-50%);
}


</style>
