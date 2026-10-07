<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/imc'

// Form data
const peso = ref<number | null>(null)
const altura = ref<number | null>(null)

// State
const loading = ref(false)
const resultado = ref<any>(null)
const historico = ref<any[]>([])
const erro = ref('')
const mostrarHistorico = ref(false)

// Classification color mapping
const classificacaoCores: Record<string, { bg: string; text: string; border: string; ring: string; emoji: string }> = {
  'Abaixo do peso': { bg: 'bg-sky-500/10', text: 'text-sky-400', border: 'border-sky-500/30', ring: 'ring-sky-500/30', emoji: '🔹' },
  'Peso normal': { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/30', ring: 'ring-emerald-500/30', emoji: '✅' },
  'Sobrepeso': { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/30', ring: 'ring-amber-500/30', emoji: '⚠️' },
  'Obesidade Grau I': { bg: 'bg-orange-500/10', text: 'text-orange-400', border: 'border-orange-500/30', ring: 'ring-orange-500/30', emoji: '🔶' },
  'Obesidade Grau II': { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/30', ring: 'ring-red-500/30', emoji: '🔴' },
  'Obesidade Grau III': { bg: 'bg-rose-500/10', text: 'text-rose-400', border: 'border-rose-500/30', ring: 'ring-rose-500/30', emoji: '🚨' },
}

// IMC gauge position (0 to 100%)
const gaugePosition = computed(() => {
  if (!resultado.value) return 0
  const imc = resultado.value.imc
  // Map IMC 10-50 to 0-100%
  const clamped = Math.min(Math.max(imc, 10), 50)
  return ((clamped - 10) / 40) * 100
})

const corResultado = computed(() => {
  if (!resultado.value) return classificacaoCores['Peso normal']
  return classificacaoCores[resultado.value.classificacao] || classificacaoCores['Peso normal']
})

async function calcular() {
  if (!peso.value || !altura.value) {
    erro.value = 'Preencha o peso e a altura'
    return
  }

  if (peso.value < 1 || peso.value > 500) {
    erro.value = 'O peso deve ser entre 1 e 500 kg'
    return
  }

  if (altura.value < 0.3 || altura.value > 3.0) {
    erro.value = 'A altura deve ser entre 0.30 e 3.00 metros'
    return
  }

  erro.value = ''
  loading.value = true

  try {
    const response = await axios.post(`${API_URL}/calcular/`, {
      peso: peso.value,
      altura: altura.value,
    })
    resultado.value = response.data
    await carregarHistorico()
  } catch (e: any) {
    if (e.response?.data) {
      const erros = Object.values(e.response.data).flat()
      erro.value = erros.join(', ')
    } else {
      erro.value = 'Erro ao conectar com o servidor. Verifique se o backend está rodando.'
    }
  } finally {
    loading.value = false
  }
}

async function carregarHistorico() {
  try {
    const response = await axios.get(`${API_URL}/historico/`)
    historico.value = response.data
  } catch (e) {
    console.error('Erro ao carregar histórico:', e)
  }
}

async function limparHistorico() {
  try {
    await axios.delete(`${API_URL}/historico/limpar/`)
    historico.value = []
    resultado.value = null
  } catch (e) {
    console.error('Erro ao limpar histórico:', e)
  }
}

function resetar() {
  peso.value = null
  altura.value = null
  resultado.value = null
  erro.value = ''
}

function formatarData(data: string) {
  return new Date(data).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  carregarHistorico()
})
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">
    <!-- Main Card -->
    <div class="relative group">
      <!-- Glow effect behind card -->
      <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-cyan-500/20 rounded-3xl blur-xl opacity-60 group-hover:opacity-80 transition-opacity duration-500"></div>

      <div class="relative bg-slate-900/80 backdrop-blur-2xl border border-white/10 rounded-3xl p-8 md:p-10 shadow-2xl">
        <!-- Input Section -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <!-- Peso -->
          <div class="space-y-2">
            <label for="peso-input" class="block text-sm font-semibold text-slate-300 tracking-wide uppercase">
              <span class="inline-flex items-center gap-2">
                <svg class="w-4 h-4 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                </svg>
                Peso
              </span>
            </label>
            <div class="relative">
              <input
                id="peso-input"
                v-model.number="peso"
                type="number"
                step="0.1"
                min="1"
                max="500"
                placeholder="72.5"
                class="w-full px-5 py-4 bg-slate-800/60 border border-white/10 rounded-2xl text-white text-lg placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all duration-300 hover:border-white/20"
                @keyup.enter="calcular"
              />
              <span class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 font-medium text-sm">kg</span>
            </div>
          </div>

          <!-- Altura -->
          <div class="space-y-2">
            <label for="altura-input" class="block text-sm font-semibold text-slate-300 tracking-wide uppercase">
              <span class="inline-flex items-center gap-2">
                <svg class="w-4 h-4 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
                Altura
              </span>
            </label>
            <div class="relative">
              <input
                id="altura-input"
                v-model.number="altura"
                type="number"
                step="0.01"
                min="0.3"
                max="3.0"
                placeholder="1.75"
                class="w-full px-5 py-4 bg-slate-800/60 border border-white/10 rounded-2xl text-white text-lg placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all duration-300 hover:border-white/20"
                @keyup.enter="calcular"
              />
              <span class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 font-medium text-sm">m</span>
            </div>
          </div>
        </div>

        <!-- Error message -->
        <Transition name="fade">
          <div v-if="erro" class="mb-6 px-5 py-3 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-400 text-sm flex items-center gap-2">
            <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {{ erro }}
          </div>
        </Transition>

        <!-- Buttons -->
        <div class="flex gap-3 mb-8">
          <button
            id="btn-calcular"
            @click="calcular"
            :disabled="loading"
            class="flex-1 px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-lg rounded-2xl shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98] cursor-pointer"
          >
            <span v-if="loading" class="inline-flex items-center gap-2">
              <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Calculando...
            </span>
            <span v-else>Calcular IMC</span>
          </button>

          <button
            v-if="resultado"
            id="btn-resetar"
            @click="resetar"
            class="px-5 py-4 bg-slate-800/80 hover:bg-slate-700/80 border border-white/10 text-slate-300 font-medium rounded-2xl transition-all duration-300 active:scale-[0.98] cursor-pointer"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>

        <!-- Result Section -->
        <Transition name="slide">
          <div v-if="resultado" class="space-y-6">
            <!-- IMC Value -->
            <div :class="['p-6 rounded-2xl border backdrop-blur-sm', corResultado.bg, corResultado.border]">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <p class="text-slate-400 text-sm font-medium mb-1">Seu IMC</p>
                  <p class="text-5xl font-bold text-white tracking-tight">
                    {{ resultado.imc.toFixed(1) }}
                  </p>
                </div>
                <div class="text-right">
                  <span class="text-4xl">{{ corResultado.emoji }}</span>
                  <p :class="['text-lg font-semibold mt-1', corResultado.text]">
                    {{ resultado.classificacao }}
                  </p>
                </div>
              </div>

              <!-- IMC Gauge Bar -->
              <div class="relative mt-5">
                <div class="h-3 rounded-full overflow-hidden flex">
                  <div class="flex-1 bg-sky-500/40"></div>
                  <div class="flex-1 bg-emerald-500/40"></div>
                  <div class="flex-1 bg-amber-500/40"></div>
                  <div class="flex-1 bg-orange-500/40"></div>
                  <div class="flex-1 bg-red-500/40"></div>
                  <div class="flex-1 bg-rose-500/40"></div>
                </div>
                <!-- Indicator -->
                <div
                  class="absolute top-1/2 -translate-y-1/2 w-5 h-5 bg-white rounded-full shadow-lg shadow-white/30 border-2 border-slate-900 transition-all duration-700 ease-out"
                  :style="{ left: `calc(${gaugePosition}% - 10px)` }"
                ></div>
                <!-- Labels -->
                <div class="flex justify-between mt-2 text-xs text-slate-500">
                  <span>Baixo</span>
                  <span>Normal</span>
                  <span>Alto</span>
                </div>
              </div>
            </div>

            <!-- Detail cards -->
            <div class="grid grid-cols-3 gap-3">
              <div class="bg-slate-800/40 border border-white/5 rounded-xl p-4 text-center">
                <p class="text-slate-500 text-xs font-medium mb-1">Peso</p>
                <p class="text-white text-lg font-bold">{{ resultado.peso }} <span class="text-slate-400 text-sm font-normal">kg</span></p>
              </div>
              <div class="bg-slate-800/40 border border-white/5 rounded-xl p-4 text-center">
                <p class="text-slate-500 text-xs font-medium mb-1">Altura</p>
                <p class="text-white text-lg font-bold">{{ resultado.altura }} <span class="text-slate-400 text-sm font-normal">m</span></p>
              </div>
              <div class="bg-slate-800/40 border border-white/5 rounded-xl p-4 text-center">
                <p class="text-slate-500 text-xs font-medium mb-1">Fórmula</p>
                <p class="text-slate-300 text-xs font-mono mt-1">P / A²</p>
              </div>
            </div>

            <!-- Classification reference table -->
            <div class="bg-slate-800/30 border border-white/5 rounded-2xl p-5">
              <p class="text-slate-400 text-sm font-semibold mb-3 uppercase tracking-wide">Tabela de Referência</p>
              <div class="space-y-2">
                <div v-for="(cores, nome) in classificacaoCores" :key="nome"
                  :class="['flex items-center justify-between px-4 py-2.5 rounded-xl transition-all duration-300',
                    resultado.classificacao === nome ? `${cores.bg} ${cores.border} border ring-1 ${cores.ring}` : 'hover:bg-slate-800/40']"
                >
                  <span class="flex items-center gap-2">
                    <span>{{ cores.emoji }}</span>
                    <span :class="resultado.classificacao === nome ? 'text-white font-semibold' : 'text-slate-400'">{{ nome }}</span>
                  </span>
                  <span :class="resultado.classificacao === nome ? cores.text + ' font-semibold' : 'text-slate-500 text-sm'">
                    {{ nome === 'Abaixo do peso' ? '< 18.5' :
                       nome === 'Peso normal' ? '18.5 - 24.9' :
                       nome === 'Sobrepeso' ? '25.0 - 29.9' :
                       nome === 'Obesidade Grau I' ? '30.0 - 34.9' :
                       nome === 'Obesidade Grau II' ? '35.0 - 39.9' :
                       '≥ 40.0' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </Transition>

        <!-- History Section -->
        <div v-if="historico.length > 0" class="mt-8 pt-6 border-t border-white/5">
          <button
            id="btn-historico"
            @click="mostrarHistorico = !mostrarHistorico"
            class="w-full flex items-center justify-between px-4 py-3 rounded-xl hover:bg-slate-800/40 transition-all duration-300 cursor-pointer"
          >
            <span class="flex items-center gap-2 text-slate-400 font-medium">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Histórico de Cálculos
              <span class="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-0.5 rounded-full">{{ historico.length }}</span>
            </span>
            <svg
              :class="['w-5 h-5 text-slate-500 transition-transform duration-300', mostrarHistorico ? 'rotate-180' : '']"
              fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <Transition name="slide">
            <div v-if="mostrarHistorico" class="mt-3 space-y-2">
              <div
                v-for="item in historico"
                :key="item.id"
                class="flex items-center justify-between px-4 py-3 bg-slate-800/30 rounded-xl border border-white/5 hover:bg-slate-800/50 transition-all duration-200"
              >
                <div class="flex items-center gap-3">
                  <span>{{ classificacaoCores[item.classificacao]?.emoji || '📊' }}</span>
                  <div>
                    <span class="text-white font-semibold">{{ item.imc.toFixed(1) }}</span>
                    <span class="text-slate-500 mx-2">·</span>
                    <span :class="classificacaoCores[item.classificacao]?.text || 'text-slate-400'" class="text-sm">
                      {{ item.classificacao }}
                    </span>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-slate-500 text-xs">{{ item.peso }}kg / {{ item.altura }}m</p>
                  <p class="text-slate-600 text-xs">{{ formatarData(item.criado_em) }}</p>
                </div>
              </div>

              <button
                id="btn-limpar-historico"
                @click="limparHistorico"
                class="w-full mt-3 px-4 py-2.5 text-red-400/70 hover:text-red-400 hover:bg-red-500/5 text-sm font-medium rounded-xl transition-all duration-300 cursor-pointer"
              >
                Limpar histórico
              </button>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Remove number input arrows */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}
</style>
