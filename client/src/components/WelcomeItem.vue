<template>
  <div class="flex bg-zinc-200/50 rounded-md dark:bg-zinc-800/50 p-2 mt-3 sm:p-3 sm:mt-5">
    <i class="flex place-content-center place-items-center size-8 text-2xl primary-gradient-text">
      <slot name="icon"></slot>
    </i>
    <div class="flex-1 ml-2 sm:ml-4">
      <h3 class="text-lg sm:text-xl font-medium mb-0 sm:mb-2">
        <slot name="heading"></slot>
      </h3>
      <p class="text-md sm:text-lg">
        <slot></slot>
      </p>
    </div>
  </div>
</template>
