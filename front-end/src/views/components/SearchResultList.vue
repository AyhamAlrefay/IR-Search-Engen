<script setup lang="ts">
import {ref, watch, reactive, computed} from 'vue'
import FILE from '@/helper/utils/file'

const props = defineProps(['searchContent'])

const emits = defineEmits<{
  (e: 'searchAuthor', val: string): void,
  (e: 'search'): void
}>()


const search = (): void => {
  emits('search')
}

let resultList: any = reactive({
  val: []
})

let sortMethod = ref('Hot')


const deleteResult = (index: number): void => {
  resultList.val.splice(index, 1)
}

const jumpUrl = (url: string) => {
  url && window.open(url)
}

const searchAuthor = (author: string): void => {
  emits('searchAuthor', author)
}

const filterResult: (target: any, option: any) => void = (target, option) => {
  resultList.val = []
  const {level, key, parent} = option
  if (Number(level) === 1) {
    getAllResult(target)
  } else if (Number(level) === 2) {
    for (let k in target[key]) {
      resultList.val = resultList.val.concat(target[key][k])
      changeSortMethod(sortMethod.value)
    }
  } else if (Number(level === 3)) {
    resultList.val = resultList.val.concat(target[parent][key])
    changeSortMethod(sortMethod.value)
  }
}

const getAllResult = (target: any): void => {
  if (Array.isArray(target)) {
    resultList.val = resultList.val.concat(target as never)
    changeSortMethod(sortMethod.value)
  } else {
    for (let k in target) {
      getAllResult(target[k])
    }
  }
}

const changeSortMethod = (method: any): void => {
  if (method === 'Year') {
    resultList.val = resultList.val.sort(
        (a: any, b: any) => Number(b.year) - Number(a.year)
    )
  } else if (method === 'Conf') {
    console.log(11)
    resultList.val = resultList.val.sort((a: any, b: any) => {
      let a1 = a.conf.toUpperCase()
      let b1 = b.conf.toUpperCase()
      if (a1 < b1) {
        return -1
      }
      if (a1 > b1) {
        return 1
      }
      return 0
    })
  }
}

// Handler pagination
type PAGE = {
  current: number
  size: number
}
const page: PAGE = reactive({
  current: 1,
  size: 200
})

const pageCurrentChange = (v: number): void => {
  page.current = v
}

const pageSizeChange = (v: number): void => {
  page.current = 1
  page.size = v
}

const virtualList = computed(() => {
  return resultList.val.slice(
      (page.current - 1) * page.size,
      page.current * page.size
  )
})

defineExpose({
  filterResult
})

const checkedMethods = ref([]);

watch(checkedMethods, (newCheckedMethods, oldCheckedMethods) => {
  const checked = newCheckedMethods.filter(x => !oldCheckedMethods.includes(x));
  const unchecked = oldCheckedMethods.filter(x => !newCheckedMethods.includes(x));

  if (checked.length > 0) {
    checked.forEach((x, i) => {
      if (x === "SpellChecker") {
        props.searchContent.spell_check = true;
      }
      if (x === "TFIDF") {
        props.searchContent.tf_idf = true;
      }
    })
    search()
    console.log('Checked:', checked);
  }
  if (unchecked.length > 0) {
    checked.forEach((x, i) => {
      if (x === "SpellChecker") {
        props.searchContent.spell_check = false;
      }
      if (x === "TFIDF") {
        props.searchContent.tf_idf = false;
      }
    })
    search()
    console.log('Unchecked:', unchecked);
  }
});

function invokeFunction() {
  // This function will be invoked whenever the checkboxes are checked or unchecked
  console.log('Current checked methods:', checkedMethods.value);
}
</script>

<template>
  <el-card class="search-result-card mb-15" shadow="never">
    <el-divider v-show="resultList.val.length > 0"/>
    <el-row
        class="mb-10 flex flex-align-center"
        v-show="resultList.val.length > 0"
    >
      <!--checkBox-->
      <span style="padding-right: 10px">Filter By:</span>
      <el-checkbox-group v-model="checkedMethods" @change="invokeFunction">
        <el-checkbox label="SpellChecker" checked></el-checkbox>
        <el-checkbox label="TFIDF" checked></el-checkbox>
      </el-checkbox-group>
    </el-row>

    <el-space class="w-100" wrap fill direction="vertical">
      <el-card
          shadow="never"
          v-for="(itm, index) in virtualList"
          :key="index"
          class="document-itm pos-relative"
      >
        <!-- Delete button -->
        <el-icon
            class="pos-absoulte delete pointer no-select"
            @click="deleteResult(index)"
        >
          <CloseBold
          />
        </el-icon>
        <el-row style="margin-bottom: -10px">
          <el-col :span="24">
            <!-- Title -->
            <el-link
                class="title"
                :href="itm.url"
                :underline="false"
                target="_blank"
            >{{ itm.title }}
            </el-link
            >
          </el-col>
        </el-row>
        <el-row class="mb-30">
          <el-col :span="24">
            <!-- Author -->
            <span
                v-for="(author, authorIndex) in itm.authors"
                :key="authorIndex"
                @click="searchAuthor(author)"
                class="mr-10"
            >
              <el-link class="author">{{ author }}</el-link>
            </span>
          </el-col>
        </el-row>
        <el-row class="mb-5">
          <el-col :span="24">
            <el-space wrap>
              <!-- Abstract -->
              <el-popover placement="top-start" :width="400" trigger="click">
              </el-popover>
              <!-- Conf -->
              <el-text class="description-style">
                {{ itm.text ? itm.text : itm.summary }}
              </el-text>
            </el-space>
          </el-col>
        </el-row>
      </el-card>
    </el-space>
    <el-empty
        v-show="resultList.val.length <= 0"
        description="No Search Result"
    ></el-empty>
    <div class="mt-15" v-show="resultList.val.length > 0">
      <el-pagination
          class="align-right"
          v-model:current-page="page.current"
          v-model:page-size="page.size"
          :page-sizes="[10, 20, 30, 50, 100, 150, 200, 300]"
          layout="sizes, prev, pager, next"
          :total="resultList.val.length"
          @size-change="pageSizeChange"
          @current-change="pageCurrentChange"
      />
    </div>
  </el-card>
</template>

<style scoped>
.search-result-card {
}

.title {
  font-size: 18px;
}

.author {
  color: #999;
  font-size: 16px;
}

.delete {
  top: 10px;
  right: 10px;
  color: #999;
}

.description-style {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: clip;
  background: #d6e9ee;
  color: black;
  border: 1px solid;
  border-radius: 5px;
  padding: 10px 10px 4px 10px;
}
</style>
