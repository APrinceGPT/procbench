<div style="padding: 1.5rem;">
	<h1 style="font-size: 1.5rem; font-weight: bold; color: white; margin: 0 0 1rem 0;">
		Help & Documentation
	</h1>

	<div style="display: flex; flex-direction: column; gap: 1.5rem;">
		<!-- Getting Started -->
		<section style="background-color: #1f2937; border-radius: 0.75rem; padding: 1.5rem;">
			<h2 style="font-size: 1.125rem; font-weight: 600; color: white; margin: 0 0 1rem 0;">
				Getting Started
			</h2>
			<ol style="list-style: decimal inside; display: flex; flex-direction: column; gap: 0.5rem; color: #9ca3af; margin: 0; padding: 0;">
				<li>Export your Process Monitor log as PML, CSV, or XML format</li>
				<li>Upload the file using the Upload page</li>
				<li>Wait for the analysis to complete</li>
				<li>Review findings on the Dashboard</li>
				<li>Investigate specific processes using the Tree or Timeline views</li>
				<li>Export a PDF report for documentation</li>
			</ol>
		</section>

		<!-- Detection Methods -->
		<section style="background-color: #1f2937; border-radius: 0.75rem; padding: 1.5rem;">
			<h2 style="font-size: 1.125rem; font-weight: 600; color: white; margin: 0 0 1rem 0;">
				Detection Methods
			</h2>
			<div style="display: flex; flex-direction: column; gap: 1rem;">
				<div>
					<h3 style="font-weight: 500; color: white; margin: 0 0 0.25rem 0;">LOLBAS Detection</h3>
					<p style="color: #9ca3af; margin: 0;">
						Identifies Living Off The Land Binaries and Scripts - legitimate Windows tools 
						commonly abused by attackers for malicious purposes.
					</p>
				</div>
				<div>
					<h3 style="font-weight: 500; color: white; margin: 0 0 0.25rem 0;">Suspicious Path Analysis</h3>
					<p style="color: #9ca3af; margin: 0;">
						Detects executables running from unusual locations like temp folders, 
						user directories, or other suspicious paths.
					</p>
				</div>
				<div>
					<h3 style="font-weight: 500; color: white; margin: 0 0 0.25rem 0;">Parent-Child Anomalies</h3>
					<p style="color: #9ca3af; margin: 0;">
						Identifies unusual parent-child process relationships that may indicate 
						process injection or lateral movement.
					</p>
				</div>
				<div>
					<h3 style="font-weight: 500; color: white; margin: 0 0 0.25rem 0;">Persistence Detection</h3>
					<p style="color: #9ca3af; margin: 0;">
						Flags processes that create or modify registry run keys and other 
						persistence mechanisms.
					</p>
				</div>
			</div>
		</section>

		<!-- Risk Levels -->
		<section style="background-color: #1f2937; border-radius: 0.75rem; padding: 1.5rem;">
			<h2 style="font-size: 1.125rem; font-weight: 600; color: white; margin: 0 0 1rem 0;">
				Understanding Risk Levels
			</h2>
			<div style="display: flex; flex-direction: column; gap: 0.75rem;">
				<div style="display: flex; align-items: center; gap: 0.75rem;">
					<span style="width: 16px; height: 16px; border-radius: 4px; background-color: #ef4444;"></span>
					<span style="font-weight: 500; color: white;">High Risk (50+)</span>
					<span style="color: #9ca3af;">- Requires immediate investigation</span>
				</div>
				<div style="display: flex; align-items: center; gap: 0.75rem;">
					<span style="width: 16px; height: 16px; border-radius: 4px; background-color: #f97316;"></span>
					<span style="font-weight: 500; color: white;">Medium Risk (20-49)</span>
					<span style="color: #9ca3af;">- Should be reviewed</span>
				</div>
				<div style="display: flex; align-items: center; gap: 0.75rem;">
					<span style="width: 16px; height: 16px; border-radius: 4px; background-color: #eab308;"></span>
					<span style="font-weight: 500; color: white;">Low Risk (1-19)</span>
					<span style="color: #9ca3af;">- May warrant attention</span>
				</div>
				<div style="display: flex; align-items: center; gap: 0.75rem;">
					<span style="width: 16px; height: 16px; border-radius: 4px; background-color: #6b7280;"></span>
					<span style="font-weight: 500; color: white;">No Risk (0)</span>
					<span style="color: #9ca3af;">- Normal activity</span>
				</div>
			</div>
		</section>

		<!-- Supported Formats -->
		<section style="background-color: #1f2937; border-radius: 0.75rem; padding: 1.5rem;">
			<h2 style="font-size: 1.125rem; font-weight: 600; color: white; margin: 0 0 1rem 0;">
				Supported File Formats
			</h2>
			<div style="display: flex; flex-direction: column; gap: 0.75rem;">
				<div>
					<span style="font-family: monospace; background-color: #374151; padding: 0.25rem 0.5rem; border-radius: 4px; color: white;">.pml</span>
					<span style="margin-left: 0.5rem; color: #9ca3af;">
						Native Process Monitor binary format (recommended)
					</span>
				</div>
				<div>
					<span style="font-family: monospace; background-color: #374151; padding: 0.25rem 0.5rem; border-radius: 4px; color: white;">.csv</span>
					<span style="margin-left: 0.5rem; color: #9ca3af;">
						Comma-separated values export
					</span>
				</div>
				<div>
					<span style="font-family: monospace; background-color: #374151; padding: 0.25rem 0.5rem; border-radius: 4px; color: white;">.xml</span>
					<span style="margin-left: 0.5rem; color: #9ca3af;">
						XML export format
					</span>
				</div>
			</div>
		</section>
	</div>
</div>
