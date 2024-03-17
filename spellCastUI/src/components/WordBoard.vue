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
import { ref, watch, toRaw } from 'vue';

const emit = defineEmits(['matrix-emitted'])
const props = defineProps({
  wordTiles: Array,
  startingTile: Array,
});

const matrix = ref(Array(5).fill().map(() => Array(5).fill('a')));
const selectedTile = ref(null);
const coloredUsedTiles = ref(props.wordTiles);
const coloredStartingTile = ref(props.startingTile);

watch(() => props.wordTiles, async (newTiles, _) => {
  coloredUsedTiles.value = newTiles
})

watch(() => props.startingTile, async (newTile, _) => {
  coloredStartingTile.value = newTile
})

function emitMatrix() {
  emit('matrix-emitted', matrix.value);
}

function handleKeydown(event, row, col) {
  const key = event.key;
  const isCharacterKey = key.length === 1;

  if (isCharacterKey) {
    // Clear the current value and set the new one
    this.matrix[row-1][col-1] = '';
  } else {
    // Handle arrow keys
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
}

function focusInput(row, col) {
  const selector = `#${CSS.escape(row + '-' + col)}`;
  const input = document.querySelector(selector);
  if (input) {
    input.focus();
  }
}

function toggleTileState(row, col) {
  const key = `${row},${col}`;
  selectedTile.value = key;
}

function getTileClass(row, col) {
  const baseClass = 'form-input border-2 border-gray-300 w-16 h-16 text-center text-xl';

  const key = `${row},${col}`;
  if (!coloredUsedTiles.value || !coloredStartingTile.value) return baseClass;

  const stringifiedStartingTile = coloredStartingTile.value.join(',');
  const stringifiedTiles = coloredUsedTiles.value.map(tile => tile.join(','));

  if (stringifiedStartingTile.includes(key))
  {
    return `bg-blue-200 ${baseClass}`;
  }
  if (stringifiedTiles.includes(key)){
    return `bg-green-200 ${baseClass}`;
  }
  return baseClass;
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
