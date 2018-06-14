def get_receipt_items(rek_response):
	interesting_items = []
	for item in rek_response['TextDetections']:

		if item['Type'] == 'LINE':

			line = item['DetectedText'].split()
			potential_value = line[-1]

			if len(line) >= 3 and '.' in potential_value:

				try:
					interesting_items.append({'item' : ' '.join(line[:2]), 'value' : float(potential_value)})
				except:
					pass

	return interesting_items
