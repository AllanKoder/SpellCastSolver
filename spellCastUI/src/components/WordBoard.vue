<template>
  <div>
    <div v-for="row in 5" :key="row" class="grid grid-cols-5 outline-2 outline-black m-auto max-w-fit">
      <input
        v-for="col in 5"
        :key="col"
        :id="`${row}-${col}`"
        v-model="matrix[row-1][col-1]"
        @change="emitMatrix"
        @click="toggleTileState(row-1, col-1)"
        @keydown="handleKeydown($event, row, col)"
        :class="getTileClass(row-1, col-1)"
        type="text"
        maxlength="1"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed  } from 'vue';

const emit = defineEmits(['matrix-emitted'])
const props = defineProps({
  mode: String
});

const matrix = ref(Array(5).fill().map(() => Array(5).fill('')));
const selectedTile = ref(null);


function emitMatrix() {
  emit('matrix-emitted', matrix.value);
}

function handleKeydown(event, row, col) {
  const key = event.key;
  if (key === 'ArrowUp' && row > 1) {
    event.preventDefault();
    focusInput(row - 1, col);
  } else if (key === 'ArrowDown' && row < 5) {
    event.preventDefault();
    focusInput(row + 1, col);
  } else if (key === 'ArrowLeft' && col > 1) {
    event.preventDefault();
    focusInput(row, col - 1);
  } else if (key === 'ArrowRight' && col < 5) {
    event.preventDefault();
    focusInput(row, col + 1);
  }
}
function focusInput(row, col) {
  const selector = `#${CSS.escape(row + '-' + col)}`;
  const input = document.querySelector(selector);
  if (input) {
    input.focus();
  }
}

function toggleTileState(row, col) {
  const key = `[${row},${col}]`;
  selectedTile.value = key;
}

const tileClasses = computed(() => {
  return {
    'double-letter': 'bg-blue-200',
    'double-word': 'bg-purple-200',
    'triple-letter': 'bg-red-200'
  };
});

function getTileClass(row, col) {
  const key = `[${row},${col}]`;
  if (selectedTile.value && selectedTile.value.key === key) {
    return `${tileClasses.value == key ? "bg-blue-200" : ""} form-input border-2 border-gray-300 w-16 h-16 text-center text-xl`;
  }
  return 'form-input border-2 border-gray-300 w-16 h-16 text-center text-xl';
}
</script>

<style>
.grid-row {
  display: flex;
}
.grid-cell {
  margin: 2px;
  width: 20px;
  height: 20px;
  text-align: center;
}
</style>
