		self.log(convert,"convert_pro")
		product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, None, convert['code'])
		self.log(product_id,"product_id")	
		compare_price = None
		if convert.get('special_price', dict()).get('price'):
			sale_price = to_decimal(convert['special_price']['price'])
			compare_price = to_decimal(convert['price'], 2)
		sku = convert['sku']
		
		if not sku:
			sku = self.convert_attribute_code(convert['name'])
		if convert['children']:
			_map = dict()
			
			index = 1
			for child in convert['children']:
				options = list()
				options_src = child['attributes']
				all_option_name = list()
				for option in options_src:
					if option['option_name'] in all_option_name:
						continue
					all_option_name.append(option['option_name'])
					_map[option['option_id']] = index
					option_target = {
						'name': option['option_name'],
						'value': option['option_value_name'],
					}
					options.append(option_target)
					index += 1
				if child.get('special_price', dict()).get('price'):
					child_sale_price = child.get('special_price', dict()).get('price')
					child_compare_price = child['price']
				else:
					child_sale_price = child['price']
					child_compare_price = compare_price
				child_sku = child['sku']
				if not child_sku:
					child_sku = sku
				sku_child_exit = self.get_map_field_by_src(self.TYPE_CHILD, code_src = child_sku)
				# child_sku = self.check_sku_exist(child_sku, type='combinations')
				variant = {
					# 'product_id': product_id,
					"options": options,
					'price': round(to_decimal(child_sale_price), 2),
					'compareToPrice': round(to_decimal(child_compare_price), 2),
					'quantity': to_int(child['qty']) if to_int(child['qty']) > 0 else 0,
					'weight': to_decimal(child['weight']),
					'sku': child_sku,
					'isShippingRequired': True
				}
				url_create_var = self.create_api_url('combinations', 'create', product_id)
				self.log(url_create_var,"url_create_var")
				if not url_create_var:
					self.log('Not create api url product id: ' + to_str(product_id), 'url_api_error')
					continue
				var_response = self.api(url_create_var, variant, 'POST', header=self.process_header(self._notice['target']['config']['extend']['header_product']))
				var_response = json_decode(var_response)
				if 'errorCode' in var_response or 'errorMessage' in var_response:
					if var_response.get('errorMessage') and 'Combination SKU is not unique' in var_response.get('errorMessage'):
						child_sku += '-' + to_str(to_int(time.time()))
						variant = {
							# 'product_id': product_id,
							"options": options,
							'price': round(to_decimal(child_sale_price), 2),
							'compareToPrice': round(to_decimal(child_compare_price), 2),
							'quantity': to_int(child['qty']) if to_int(child['qty']) > 0 else 0,
							'weight': child['weight'],
							'sku': child_sku,
							'isShippingRequired': True
						}
						url_create_var = self.create_api_url('combinations', 'create', product_id)
						if not url_create_var:
							self.log('Not create api url product id: ' + to_str(product_id), 'url_api_error')
							continue
						var_response = self.api(url_create_var, variant, 'POST', header=self.process_header(self._notice['target']['config']['extend']['header_product']))
						var_response = json_decode(var_response)
						if 'errorCode' in var_response or 'errorMessage' in var_response:
							self.log(
								var_response['errorMessage'] + ' sku: ' + to_str(child_sku) + ' product id: ' + to_str(
									product_id), 'varitant_error')
						else:
							self.insert_map(self.TYPE_CHILD, child['id'], var_response.get('id'), convert['sku'], child_sku)
							self.list_sku_old.append(child_sku)
					else:
						self.log(var_response['errorMessage'] + ' sku: ' + to_str(child_sku) + ' product id: ' + to_str(product_id), 'varitant_error')
				else:
					self.insert_map(self.TYPE_CHILD, child['id'], var_response.get('id'), convert['sku'], child_sku)
					self.list_sku_old.append(child_sku)
				if not var_response.get('id'):
					continue
				if child['thumb_image']['url']:
					main_image = self.process_image_before_import(child['thumb_image']['url'], child['thumb_image']['path'])
					if main_image:
						url_create_image_var = self.create_api_url('combinations', 'image', product_id, var_response.get('id'), url_image = main_image['url'])
						self.log(url_create_image_var,"url_create_image_var")
						response_image = self.api(url_create_image_var, None, 'POST', header=self.process_header(self._notice['target']['config']['extend']['image_header_product']))
						response_image = json_decode(response_image)
						if not response_image or 'errorCode' in response_image:
							self.log('Image ' + to_str(main_image['url']) + ' product id: ' + to_str(product_id), 'image_error')
