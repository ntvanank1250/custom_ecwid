		self.log(convert,"convert_pro")
		product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
		self.log(product_id,"product_id")
		main_image = None
		if convert['thumb_image']['url']:
			thumb_image = self.process_image_before_import(convert['thumb_image']['url'], convert['thumb_image']['path'])
			if thumb_image:
				url_image_thumb_product = self.create_api_url('product', 'image', product_id, url_image = thumb_image['url'])
				response_image = self.api(url_image_thumb_product, None, 'POST', header=self.process_header(self._notice['target']['config']['extend']['image_header_product']))
				response_image = json_decode(response_image)
				if not response_image or 'errorCode' in response_image:
					self.log('Image ' + to_str(thumb_image['url']) + ' product id: ' + to_str(product_id), 'image_error')
		for image in convert['images']:
			product_image = self.process_image_before_import(image['url'], image['path'])
			if product_image:
				url_image_product = self.create_api_url('product', 'gallery', product_id, url_image = product_image['url'])
				response_image = self.api(url_image_product, None, 'POST', header=self.process_header(self._notice['target']['config']['extend']['image_header_product']))
				response_image = json_decode(response_image)
				if not response_image or 'errorCode' in response_image:
					self.log('Image ' + to_str(product_image['url']) + ' product id: ' + to_str(product_id), 'image_error')

