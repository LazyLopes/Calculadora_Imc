<script setup lang="ts">
import { ref, computed } from 'vue'
import ImcCalculator from './components/ImcCalculator.vue'
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950 relative overflow-hidden">
    <!-- Animated background orbs -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -left-40 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute top-1/3 -right-20 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute -bottom-20 left-1/3 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" style="animation-delay: 2s;"></div>
    </div>

    <!-- Grid pattern overlay -->
    <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(circle, #fff 1px, transparent 1px); background-size: 40px 40px;"></div>

    <!-- Content -->
    <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 py-12">
      <!-- Header -->
      <header class="text-center mb-10">
        <div class="inline-flex items-center gap-2 mb-4 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 backdrop-blur-sm">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-indigo-300 text-sm font-medium tracking-wide">Calculadora Online</span>
        </div>
        <h1 class="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-indigo-200 to-purple-300 bg-clip-text text-transparent mb-3 tracking-tight">
          Índice de Massa<br/>Corporal
        </h1>
        <p class="text-slate-400 text-lg max-w-md mx-auto leading-relaxed">
          Descubra seu IMC e receba uma análise completa da sua composição corporal
        </p>
      </header>

      <!-- Calculator -->
      <ImcCalculator />

    </div>
  </div>
</template>
