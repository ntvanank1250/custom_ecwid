		type_action = action
		api_url = False
		if not type_entity or not action:
			return api_url
		if action == 'search':
			type_action = 'url'
		action_entity = to_str(type_action).lower() + '_' + to_str(type_entity).lower()
		if self._notice['target']['config']['extend'].get(action_entity):
			api_url = self._notice['target']['config']['extend'].get(action_entity)
			if entity_id:
				api_url = to_str(api_url).replace('SET-' + to_str(type_entity).upper() + '-ID', to_str(entity_id))
			if action == 'search' and sku:
				api_url = to_str(api_url).replace('?', '?sku=') + to_str(sku) + '&'

		if type_entity == 'product' and entity_id:	
			if to_str(type_action).lower() == 'image' and entity_com_id:
				api_url = to_str(self._notice['target']['config']['extend']['image_product']).replace('SET-PRODUCT-ID', to_str(entity_id), to_str(entity_id)) 
				self.log(api_url,"url_create_image_pro")
			if to_str(type_action).lower() == 'gallery':
				api_url = to_str(self._notice['target']['config']['extend']['image_product']).replace('image', 'gallery').replace('SET-PRODUCT-ID', to_str(entity_id))
				self.log(api_url,"url_create_image_pro")

		if type_entity == 'combinations' and entity_id:
			if to_str(type_action).lower() == 'create':
				urls = self._notice['target']['config']['extend']['create_product']
				api_url = to_str(urls).replace('?', '') + '/' + to_str(entity_id) + '/combinations?'
				self.log(url_create_image_var,"url_create_image_var")

			if to_str(type_action).lower() == 'image' and entity_com_id:
				urls = self._notice['target']['config']['extend']['image_product']
				api_url = to_str(urls).replace('/SET-PRODUCT-ID/image?', '') +'/' + to_str(entity_id) + '/combinations/' + to_str(entity_com_id) + '/image?'
				self.log(api_url,"url_create_image_var")
		if api_url and url_image:
			api_url += '?externalUrl=' + to_str(url_image)
			self.log(api_url,"url_create_image_pro")
