<div class="p-6">
	<h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
		Help & Documentation
	</h1>

	<div class="space-y-6">
		<!-- Getting Started -->
		<section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
			<h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
				Getting Started
			</h2>
			<ol class="list-decimal list-inside space-y-2 text-gray-600 dark:text-gray-400">
				<li>Export your Process Monitor log as PML, CSV, or XML format</li>
				<li>Upload the file using the Upload page</li>
				<li>Wait for the analysis to complete</li>
				<li>Review findings on the Dashboard</li>
				<li>Investigate specific processes using the Tree or Timeline views</li>
				<li>Export a PDF report for documentation</li>
			</ol>
		</section>

		<!-- Detection Methods -->
		<section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
			<h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
				Detection Methods
			</h2>
			<div class="space-y-4">
				<div>
					<h3 class="font-medium text-gray-900 dark:text-white">LOLBAS Detection</h3>
					<p class="text-gray-600 dark:text-gray-400">
						Identifies Living Off The Land Binaries and Scripts - legitimate Windows tools 
						commonly abused by attackers for malicious purposes.
					</p>
				</div>
				<div>
					<h3 class="font-medium text-gray-900 dark:text-white">Suspicious Path Analysis</h3>
					<p class="text-gray-600 dark:text-gray-400">
						Detects executables running from unusual locations like temp folders, 
						user directories, or other suspicious paths.
					</p>
				</div>
				<div>
					<h3 class="font-medium text-gray-900 dark:text-white">Parent-Child Anomalies</h3>
					<p class="text-gray-600 dark:text-gray-400">
						Identifies unusual parent-child process relationships that may indicate 
						process injection or lateral movement.
					</p>
				</div>
				<div>
					<h3 class="font-medium text-gray-900 dark:text-white">Persistence Detection</h3>
					<p class="text-gray-600 dark:text-gray-400">
						Flags processes that create or modify registry run keys and other 
						persistence mechanisms.
					</p>
				</div>
			</div>
		</section>

		<!-- Risk Levels -->
		<section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
			<h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
				Understanding Risk Levels
			</h2>
			<div class="space-y-3">
				<div class="flex items-center gap-3">
					<span class="w-4 h-4 rounded bg-red-500"></span>
					<span class="font-medium text-gray-900 dark:text-white">High Risk (50+)</span>
					<span class="text-gray-600 dark:text-gray-400">- Requires immediate investigation</span>
				</div>
				<div class="flex items-center gap-3">
					<span class="w-4 h-4 rounded bg-orange-500"></span>
					<span class="font-medium text-gray-900 dark:text-white">Medium Risk (20-49)</span>
					<span class="text-gray-600 dark:text-gray-400">- Should be reviewed</span>
				</div>
				<div class="flex items-center gap-3">
					<span class="w-4 h-4 rounded bg-yellow-500"></span>
					<span class="font-medium text-gray-900 dark:text-white">Low Risk (1-19)</span>
					<span class="text-gray-600 dark:text-gray-400">- May warrant attention</span>
				</div>
				<div class="flex items-center gap-3">
					<span class="w-4 h-4 rounded bg-gray-400"></span>
					<span class="font-medium text-gray-900 dark:text-white">No Risk (0)</span>
					<span class="text-gray-600 dark:text-gray-400">- Normal activity</span>
				</div>
			</div>
		</section>

		<!-- Supported Formats -->
		<section class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
			<h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
				Supported File Formats
			</h2>
			<div class="space-y-3">
				<div>
					<span class="font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">.pml</span>
					<span class="ml-2 text-gray-600 dark:text-gray-400">
						Native Process Monitor binary format (recommended)
					</span>
				</div>
				<div>
					<span class="font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">.csv</span>
					<span class="ml-2 text-gray-600 dark:text-gray-400">
						Comma-separated values export
					</span>
				</div>
				<div>
					<span class="font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">.xml</span>
					<span class="ml-2 text-gray-600 dark:text-gray-400">
						XML export format
					</span>
				</div>
			</div>
		</section>
	</div>
</div>
