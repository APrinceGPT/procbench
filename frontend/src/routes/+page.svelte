<script lang="ts">
	import FileUpload from '$lib/components/upload/FileUpload.svelte';
</script>

<div class="min-h-screen flex flex-col">
	<!-- Header -->
	<header class="bg-white dark:bg-gray-800 shadow-sm">
		<div class="max-w-7xl mx-auto py-6 px-4">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white">
				ProcBench
			</h1>
			<p class="mt-1 text-gray-600 dark:text-gray-400">
				AI-powered Process Monitor log analysis for SOC analysts
			</p>
		</div>
	</header>

	<!-- Main content -->
	<main class="flex-1 flex items-center justify-center p-8">
		<div class="max-w-3xl w-full">
			<div class="text-center mb-8">
				<h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
					Upload Process Monitor Log
				</h2>
				<p class="text-gray-600 dark:text-gray-400">
					Turn process noise into threat signal. Upload your PML, CSV, or XML log file to get started.
				</p>
			</div>

			<FileUpload />

			<!-- Features -->
			<div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
				<div class="text-center p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm">
					<div class="w-12 h-12 mx-auto mb-4 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
						<svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
						</svg>
					</div>
					<h3 class="font-semibold text-gray-900 dark:text-white">LOLBAS Detection</h3>
					<p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
						Identifies living-off-the-land binaries used by attackers
					</p>
				</div>

				<div class="text-center p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm">
					<div class="w-12 h-12 mx-auto mb-4 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
						<svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
						</svg>
					</div>
					<h3 class="font-semibold text-gray-900 dark:text-white">AI Analysis</h3>
					<p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
						AI-powered reasoning for suspicious process behavior
					</p>
				</div>

				<div class="text-center p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm">
					<div class="w-12 h-12 mx-auto mb-4 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
						<svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
						</svg>
					</div>
					<h3 class="font-semibold text-gray-900 dark:text-white">PDF Reports</h3>
					<p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
						Export professional reports for stakeholders
					</p>
				</div>
			</div>
		</div>
	</main>

	<!-- Footer -->
	<footer class="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-4">
		<div class="max-w-7xl mx-auto px-4 text-center text-sm text-gray-500 dark:text-gray-400">
			ProcBench v1.0 - Process Monitor Analysis Platform
		</div>
	</footer>
</div>
