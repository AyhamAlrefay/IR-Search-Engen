<script setup lang="ts">
import {reactive, ref} from 'vue'
import {useDark, useToggle} from '@vueuse/core'
import {ElLoading, ElMessage} from 'element-plus'
import AdvancedSettingDlg from '@/views/components/AdvancedSettingDlg.vue'
import SearchResultList from '@/views/components/SearchResultList.vue'
import {documentSearch, getSuggestion} from '@/helper/api/document.js'
import AutoComplete from "@/views/components/AutoComplete.vue";
import LogoComponent from "@/views/components/LogoComponent.vue";


interface SearchResult {
  "doc_id": string,
  "title": string,
  "text": string,
  "stance": string,
  "url": string,
  "condition": string,
  "detailed_description": string,
  "eligibility": string,
  "summary": string,
}

// First entry
let firstEntry = ref(true)
// Query content
let searchContent = reactive({
  query: '',
  searchtype: 'Beir',
  spell_check: true,
  tf_idf: true,
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

interface SearchRequest {
  "query": string,
  "dataset_name": string,
  "spell_check": true,
  "tf_idf": true
}

// Query result
let queryResult = reactive({
  val: {}
})
// Advanced setting dialog
const settingDlg = ref(null)
// Search result component
const searchResult = ref(null)


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
  documentSearch(
      {page: 1},
      {
        dataset_name: searchContent.searchtype.toLowerCase(),
        query: searchContent.query,
        spell_check: true,
        tf_idf: true
      } as SearchRequest
      // {
      // ...searchContent,
      // confs: searchContent.confs.join(',')
      // }
  )
      .then((res: any) => {
        // const searchResult: SearchResult[] = res.results.map((item: SearchResult) => {
        //   return item;
        // });
        const searchResult: SearchResult[] = res.results as SearchResult[];

        // if (msg === 'success') {
        queryResult.val = searchResult
        handleTreeClick({level: 1})
        // }
      })
      .catch(err => {
        console.log(err)
      })
      .finally(() => {
        firstEntry.value = false
        loading && loading.close()
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
      <el-link type="primary" :icon="isDark ? 'Sunny' : 'Moon'" @click="toggleDark()" class="icon-size">
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
        <SearchResultList ref="searchResult" @search-author="handleSearchAuthor"
                          v-model:search-content="searchContent" @search="search"/>
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

.icon-size {
  font-size: 1.5rem;
}


</style>
