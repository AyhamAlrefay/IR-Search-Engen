<template>
  <div class="flex gap-4">
    <el-autocomplete
        v-model="searchContent.query"
        :fetch-suggestions="querySearchAsync"
        :trigger-on-focus="false"
        clearable
        placeholder="Input your keywords"
        @select="handleSelect"
        @keyup.enter="search"
    >
      <template #prepend>
        <el-select v-model="searchContent.searchtype" placeholder="Select" style="width: 100px" size="large">
          <el-option v-for="(itm, index) in SEARCH_TYPE_LIST" :key="index" :label="itm.label"
                     :value="itm.value"/>
        </el-select>
      </template>
      <template #append>
        <el-button icon="Search" @click="search"/>
      </template>
      <template #loading>
        <el-icon class="is-loading">
          <svg class="circular" viewBox="0 0 20 20">
            <g
                class="path2 loading-path"
                stroke-width="0"
                style="animation: none; stroke: none"
            >
              <circle r="3.375" class="dot1" cx="0" cy="0"/>
              <circle r="3.375" class="dot2" cx="0" cy="0"/>
              <circle r="3.375" class="dot4" cx="0" cy="0"/>
              <circle r="3.375" class="dot3" cx="0" cy="0"/>
            </g>
          </svg>
        </el-icon>
      </template>
    </el-autocomplete>
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue'


const emits = defineEmits<{
  (e: 'search'): void
}>()


const search = (): void => {
  emits('search')
}

const props = defineProps(['searchContent'])


// Search type list
const SEARCH_TYPE_LIST = [
  {label: 'Beir', value: 'title'},
  {label: 'Clinicaltrials', value: 'author'}
]

const state = ref('')

interface LinkItem {
  value: string
  link: string
}

const links = ref<LinkItem[]>([])

const loadAll = () => {
  return [
    {value: 'vue', link: 'https://github.com/vuejs/vue'},
    {value: 'element', link: 'https://github.com/ElemeFE/element'},
    {value: 'cooking', link: 'https://github.com/ElemeFE/cooking'},
    {value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui'},
    {value: 'vuex', link: 'https://github.com/vuejs/vuex'},
    {value: 'vue-router', link: 'https://github.com/vuejs/vue-router'},
    {value: 'babel', link: 'https://github.com/babel/babel'},
  ]
}

let timeout: ReturnType<typeof setTimeout>
const querySearchAsync = (queryString: string, cb: (arg: any) => void) => {
  const results = queryString
      ? links.value.filter(createFilter(queryString))
      : links.value

  clearTimeout(timeout)
  timeout = setTimeout(() => {
    cb(results)
  }, 1000 * Math.random())
}
const createFilter = (queryString: string) => {
  return (restaurant: LinkItem) => {
    return (
        restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}

const handleSelect = (item: Record<string, any>) => {
  console.log(item)
}

onMounted(() => {
  links.value = loadAll()
})
</script>

<style>
.circular {
  display: inline;
  height: 30px;
  width: 30px;
  animation: loading-rotate 2s linear infinite;
}

.path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-color-primary);
  stroke-linecap: round;
}

.loading-path .dot1 {
  transform: translate(3.75px, 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
}

.loading-path .dot2 {
  transform: translate(calc(100% - 3.75px), 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.4s;
}

.loading-path .dot3 {
  transform: translate(3.75px, calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 1.2s;
}

.loading-path .dot4 {
  transform: translate(calc(100% - 3.75px), calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.8s;
}

@keyframes loading-rotate {
  to {
    transform: rotate(360deg);
  }
}

@keyframes loading-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -40px;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -120px;
  }
}

@keyframes custom-spin-move {
  to {
    opacity: 1;
  }
}
</style>
