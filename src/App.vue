<template>
  <header>
    <h1>Smartisan Icons</h1>
    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchKeyword" 
        class="search-input" 
        placeholder="搜索图标..."
      >
    </div>
  </header>

  <div class="container">
    <!-- 页面加载遮罩 -->
    <div v-if="loading" class="page-loader">
      <div class="loader-spinner"></div>
      <div class="loader-text">加载图标库...</div>
    </div>

    <div class="icon-grid" v-show="!loading">
      <div v-for="icon in paginatedIcons" :key="icon.filename" class="icon-card" :title="icon.displayName">
        <div class="icon-image-wrapper" :class="{ loading: !icon.loaded }">
          <img 
            :src="icon.path" 
            :alt="icon.displayName" 
            :title="icon.displayName"
            loading="lazy" 
            :id="'img-' + icon.filename"
            @load="handleImageLoad(icon)"
            :class="{ loaded: icon.loaded }"
          >
        </div>
        <div class="icon-name" :title="icon.displayName">{{ icon.displayName }}</div>
        
        <div class="icon-actions">
          <button class="action-btn" @click="handleCopy(icon.path, '图片路径已复制')">复制路径</button>
          <button class="action-btn" @click="handleCopy(icon.displayName, '图片名称已复制')">复制名称</button>
          <button class="action-btn" @click="handleBase64(icon)">复制 Base64</button>
        </div>
      </div>
      
      <div v-if="paginatedIcons.length === 0" style="text-align:center; grid-column: 1/-1; padding: 50px; color: #999;">
        没有找到匹配的图标
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        class="page-btn" 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >←</button>

      <template v-for="page in paginationRange" :key="page">
        <button 
          v-if="page !== '...'"
          class="page-btn" 
          :class="{ active: currentPage === page }"
          @click="changePage(page)"
        >{{ page }}</button>
        <span v-else class="page-dots">...</span>
      </template>

      <button 
        class="page-btn" 
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >→</button>
    </div>
  </div>

  <!-- 提示框容器 -->
  <div id="toast-container"></div>
</template>

<script setup>
import { ref, computed, onMounted, watch, reactive } from 'vue'

const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = 60
const iconMap = ref({})
const allIcons = ref([]) // 初始化为空，等待加载
const loading = ref(true) // 页面级加载状态

// 图片加载状态字典，使用 reactive 保证响应性
const imageLoadStatus = reactive({})

// 加载映射文件
onMounted(async () => {
  try {
    // 动态加载 data.js
    // 为了兼容，我们假设 data.js 在 public 目录下，并且定义了 window.icons
    // 但在 Vite 工程化中，最好的方式是让 update_icon_data.py 生成 json
    // 或者我们在这里手动 fetch 它，或者 import 它
    // 由于 data.js 内容是 "window.icons = [...]"，我们可以通过 script 标签加载，或者 fetch 并 eval (不推荐)
    // 更好的方式是 fetch 一个 JSON。为了兼容旧逻辑，我们先尝试动态插入 script 标签加载 data.js
    
    await loadScript('data.js')
    const rawIcons = window.icons || []

    const response = await fetch('app_icon_map.json')
    const mapData = await response.json()

    const map = {}
    const orderedList = []
    const stemToFilename = {}
    const remainingFiles = new Set(rawIcons)

    rawIcons.forEach(filename => {
        const stem = filename.replace(/\.[^/.]+$/, "")
        stemToFilename[stem] = filename
    })

    Object.entries(mapData).forEach(([displayName, filenames]) => {
        const stems = Array.isArray(filenames) ? filenames : [filenames]
        stems.forEach(stem => {
            map[stem] = displayName
            const filename = stemToFilename[stem]
            if (filename && remainingFiles.has(filename)) {
                orderedList.push(filename)
                remainingFiles.delete(filename)
            }
        })
    })

    const remainingList = Array.from(remainingFiles).sort()
    
    iconMap.value = map
    allIcons.value = [...orderedList, ...remainingList]
    loading.value = false
  } catch (err) {
    console.error('加载资源失败:', err)
    loading.value = false
  }
})

// 辅助函数：动态加载 script
function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = src
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

// 搜索过滤
const filteredIcons = computed(() => {
    const keyword = searchKeyword.value.toLowerCase().trim()
    if (!keyword) return allIcons.value

    return allIcons.value.filter(filename => {
        const fileStem = filename.replace(/\.[^/.]+$/, "")
        const displayName = iconMap.value[fileStem] || filename
        return filename.toLowerCase().includes(keyword) || 
               displayName.toLowerCase().includes(keyword)
    })
})

// 搜索时重置页码
watch(searchKeyword, () => {
    currentPage.value = 1
})

// 分页数据
const paginatedIcons = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    const end = start + pageSize
    return filteredIcons.value.slice(start, end).map(filename => {
        const fileStem = filename.replace(/\.[^/.]+$/, "")
        const displayName = iconMap.value[fileStem] || filename
        // 路径逻辑
        const path = `icon/${filename}`
        
        return {
            filename,
            displayName,
            path,
            loaded: !!imageLoadStatus[filename] // 获取加载状态
        }
    })
})

// 处理图片加载完成
const handleImageLoad = (icon) => {
    imageLoadStatus[icon.filename] = true
}

const totalPages = computed(() => Math.ceil(filteredIcons.value.length / pageSize))

// 分页范围逻辑
const paginationRange = computed(() => {
    const total = totalPages.value
    const current = currentPage.value
    const range = 2
    const res = []

    for (let i = 1; i <= total; i++) {
        if (i === 1 || i === total || (i >= current - range && i <= current + range)) {
            res.push(i)
        } else if (i === current - range - 1 || i === current + range + 1) {
            res.push('...')
        }
    }
    return res
})

// 方法
const changePage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
}

const handleCopy = (text, msg) => {
    // 如果是相对路径，转换为绝对路径
    if (text.startsWith && text.startsWith('icon/')) {
         text = new URL(text, window.location.href).href
    }
    
    navigator.clipboard.writeText(text).then(() => {
        showToast(msg)
    }).catch(err => {
        console.error('复制失败:', err)
        alert('复制失败，请重试')
    })
}

const handleBase64 = (icon) => {
    const img = document.getElementById('img-' + icon.filename)
    if (img) {
        convertImageToBase64(img, (base64) => {
            if (base64) {
                navigator.clipboard.writeText(base64).then(() => {
                    showToast('Base64 已复制')
                })
            } else {
                alert('Base64 转换失败')
            }
        })
    }
}

const showToast = (msg) => {
    const container = document.getElementById('toast-container')
    const toast = document.createElement('div')
    toast.style.position = 'fixed'
    toast.style.top = '20px'
    toast.style.left = '50%'
    toast.style.transform = 'translateX(-50%)'
    toast.style.background = 'rgba(0,0,0,0.8)'
    toast.style.color = '#fff'
    toast.style.padding = '10px 20px'
    toast.style.borderRadius = '4px'
    toast.style.zIndex = '1000'
    toast.innerText = msg
    container.appendChild(toast)
    setTimeout(() => toast.remove(), 2000)
}

const convertImageToBase64 = (img, callback) => {
    if (!img.complete) {
        img.onload = () => convertImageToBase64(img, callback)
        return
    }
    try {
        const canvas = document.createElement('canvas')
        canvas.width = img.naturalWidth
        canvas.height = img.naturalHeight
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0)
        const dataURL = canvas.toDataURL('image/png')
        callback(dataURL)
    } catch (e) {
        console.error('Base64 conversion failed', e)
        fetch(img.src)
            .then(response => response.blob())
            .then(blob => {
                const reader = new FileReader()
                reader.onloadend = () => callback(reader.result)
                reader.readAsDataURL(blob)
            })
            .catch(err => {
                console.error('Fetch failed', err)
                callback(null)
            })
    }
}
</script>

<style src="./style.css"></style>
