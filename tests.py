from unittest import TestCase
from distance import Distance



class InitTests(TestCase):
	
	def test_is_instance(self):
		dist = Distance("euclidean", 1,3,5)
		self.assertIsInstance(dist,Distance)
		
	def test_metric_keyerror(self):
		with self.assertRaises(KeyError):
			Distance("fake_metric", 2,3,5,5)

	def test_args_valueerror(self):
		with self.assertRaises(ValueError):
			Distance("cosine")
		
		inputs = [[ 1, "2", 3], [True, [], 3.], [9.3, 1., set()], {"e": "1"}]
		
		for inp in inputs:
			with self.subTest(text = inp), self.assertRaises(ValueError):
				Distance("manhattan", (inp))
			
	def test_unfit_distance(self):
		dist = Distance("cosine", 2,4,4)
		self.assertFalse(dist.has_distance())
		self.assertEqual(0, dist.distance)	
		
		
		
class ManhattanTests(TestCase):
	
	def test_manhattan(self):
		man_dist = Distance("manhattan", 1, 0)
		self.assertEqual("manhattan", man_dist.metric)
		_ = man_dist.distance_calculator()
		self.assertTrue(man_dist.has_distance())
	
	def test_outputs(self):
		metric = "manhattan"
		
		self.assertEqual(6, Distance(metric, 1,2,3).distance_calculator())
		self.assertEqual(1, Distance(metric, 1,0).distance_calculator())
		self.assertEqual(31, Distance(metric, 9, 10, 12).distance_calculator())
		self.assertEqual(8, Distance(metric, -1,2,-5).distance_calculator())
		self.assertEqual(41, Distance(metric, 1,2,6,12, -20).distance_calculator())
		self.assertEqual(15.3, Distance(metric, -3.4, 5.1, -6.8).distance_calculator())
		self.assertEqual(29.1, Distance(metric, 10.4, -2.2, 9.7, -6.8).distance_calculator())
		
class EuclideanTests(TestCase):
	
	def test_euclidean(self):
		euc_dist = Distance("euclidean", 1, 0)
		self.assertTrue("euclidean", euc_dist.metric)
		_ = euc_dist.distance_calculator()
		self.assertTrue(euc_dist.has_distance())	
	
	def test_outputs(self):
		metric = "euclidean"
		
		self.assertEqual(3.742, Distance(metric, 1,2,3).distance_calculator())
		self.assertEqual(1, Distance(metric, 1,0).distance_calculator())
		self.assertEqual(18.028, Distance(metric, 9, 10, 12).distance_calculator())
		self.assertEqual(5.477, Distance(metric, -1,2,-5).distance_calculator())
		self.assertEqual(24.187, Distance(metric, 1,2,6,12, -20).distance_calculator())
		self.assertEqual(9.155, Distance(metric, -3.4, 5.1, -6.8).distance_calculator())
		self.assertEqual(15.916, Distance(metric, 10.4, -2.2, 9.7, -6.8).distance_calculator())
		
class CosineTests(TestCase):
	def test_cosine(self):
		cos_dist = Distance("cosine", 1, 0)
		self.assertTrue("cosine", cos_dist.metric)
		_ = cos_dist.distance_calculator()
		self.assertTrue(cos_dist.has_distance())	
	
	def test_outputs(self):
		metric = "cosine"
		
		self.assertEqual(0.598, Distance(metric, 1,2,3).distance_calculator())
		self.assertEqual(0.707, Distance(metric, 1,1).distance_calculator())
		self.assertEqual(0.746, Distance(metric, 9, 10, 12).distance_calculator())
		self.assertEqual(0.408, Distance(metric, -1,2,-5).distance_calculator())
		self.assertEqual(0.562, Distance(metric, 1,2,6,12, -20).distance_calculator())
		self.assertEqual(0.67, Distance(metric, -3.4, 5.1, -6.8).distance_calculator())
		self.assertEqual(0.904, Distance(metric, 10.4, -2.2, 9.7, -6.8).distance_calculator())
		
class ConcatenateTests(TestCase):
	def test_concatenation_error(self):
		
		euc_dist = Distance("euclidean", 1,2)
		cos_dist = Distance("cosine", 3,4)
		with self.assertRaises(TypeError):
			euc_dist.concatenate(cos_dist)
		with self.assertRaises(TypeError):
			cos_dist.concatenate(euc_dist)
			
	def test_concatenation(self):
		metric = "euclidean"
		ed1 = Distance(metric, 1,2)
		ed2 = Distance(metric, 3,4)
		ed12 = ed1.concatenate(ed2)
		
		self.assertEqual([1,2,3,4], ed12.nums)
		
		metric = "manhattan"
		md1 = Distance(metric, 1,2)
		md2 = Distance(metric, 3,4)
		md12 = md1.concatenate(md2)

		self.assertEqual([1,2,3,4], md12.nums)
		
class MagicMethodTests(TestCase):
	
	def test_str(self):
		dist = Distance("cosine", 8, 9)
		_ = dist.distance_calculator()
		self.assertEqual(dist.__str__(), 'The cosine distance for the set of numbers [8, 9] is 0.664')
		
	def test_repr(self):
		dist = Distance("cosine", 8, 9)
		self.assertEqual(dist.__repr__(), 'Distance: [8, 9]')
		
	def test_add(self):
		
		dist1 = Distance("euclidean", 30, 40)
		dist2 = Distance("cosine", 10, 20)
		with self.assertRaises(TypeError):
			dist1 + dist2
		dist3 = Distance("euclidean", 50, 75)
		_ = dist3.distance_calculator()
		
		with self.assertRaises(ValueError):
			dist1 + dist3
			
		ed1 = Distance("euclidean", 3, 4)
		ed2 = Distance("euclidean", 6, 8)
		ed_dist1 = ed1.distance_calculator()
		ed_dist2 = ed2.distance_calculator()
		self.assertEqual(ed_dist1 + ed_dist2, ed1 + ed2)
		
		md1 = Distance("manhattan", 12, 16)
		md2 = Distance("manhattan", 5, 10)
		md_dist1 = md1.distance_calculator()
		md_dist2 = md2.distance_calculator()
		self.assertEqual(md_dist1 + md_dist2, md1 + md2)
		
	def test_sub(self):
		dist1 = Distance("euclidean", 30, 40)
		dist2 = Distance("cosine", 10, 20)
		with self.assertRaises(TypeError):
			dist1 - dist2
			
		dist3 = Distance("euclidean", 50, 75)
		_ = dist3.distance_calculator()
		
		with self.assertRaises(ValueError):
			dist1 - dist3
			
		ed1 = Distance("euclidean", 3, 4)
		ed2 = Distance("euclidean", 6, 8)
		ed_dist1 = ed1.distance_calculator()
		ed_dist2 = ed2.distance_calculator()
		self.assertEqual(ed_dist1 - ed_dist2, ed1 - ed2)
		
		md1 = Distance("manhattan", 12, 16)
		md2 = Distance("manhattan", 5, 10)
		md_dist1 = md1.distance_calculator()
		md_dist2 = md2.distance_calculator()
		self.assertEqual(md_dist1 - md_dist2, md1 - md2)
		
	def test_equals(self):
		dist1 = Distance("euclidean", 30, 40)
		dist2 = Distance("cosine", 10, 20)
		with self.assertRaises(TypeError):
			dist1 == dist2
			
		dist3 = Distance("euclidean", 50, 75)
		_ = dist3.distance_calculator()
		
		with self.assertRaises(ValueError):
			dist1 == dist3
			
		#manhattan
		args1 = [7,8,9]
		args2 = [-7,8,9]
		md1 = Distance("manhattan",*args1)
		md2 = Distance("manhattan",*args2)
		_ = md1.distance_calculator()
		_ = md2.distance_calculator()	
		self.assertEqual(md1, md2)
		
		#euclidean
		args1 = [12,16]
		args2 = [-12,16]
		ed1 = Distance("euclidean",*args1)
		ed2 = Distance("euclidean",*args2)
		_ = ed1.distance_calculator()
		_ = ed2.distance_calculator()
		self.assertEqual(ed1, ed2)
		
		#cosine 
		args1 = [2, 2]
		args2 = [1, 1]
		cd1 = Distance("cosine", *args1)
		cd2 = Distance("cosine", *args2)
		_ = cd1.distance_calculator()
		_ = cd2.distance_calculator()
		self.assertEqual(cd1, cd2)
		
	def test_greater_than(self):
		dist1 = Distance("euclidean", 30, 40)
		dist2 = Distance("cosine", 10, 20)
		with self.assertRaises(TypeError):
			dist1 > dist2
			
		dist3 = Distance("euclidean", 50, 75)
		_ = dist3.distance_calculator()
		
		with self.assertRaises(ValueError):
			dist1 > dist3
			
		#manhattan
		args1 = [7,8,10]
		args2 = [-7,8,9]
		md1 = Distance("manhattan",*args1)
		md2 = Distance("manhattan",*args2)
		_ = md1.distance_calculator()
		_ = md2.distance_calculator()	
		self.assertTrue(md1 > md2)
		
		#euclidean
		args1 = [12,17]
		args2 = [-12,16]
		ed1 = Distance("euclidean",*args1)
		ed2 = Distance("euclidean",*args2)
		_ = ed1.distance_calculator()
		_ = ed2.distance_calculator()
		self.assertTrue(ed1 > ed2)
		
		#cosine
		args1 = [8, 8]
		args2 = [8, 4]
		cd1 = Distance("cosine", *args1)
		cd2 = Distance("cosine", *args2)
		_ = cd1.distance_calculator()
		_ = cd2.distance_calculator()
		self.assertTrue(cd1 > cd2)
		
	def test_less_than(self):
		dist1 = Distance("euclidean", 30, 40)
		dist2 = Distance("cosine", 10, 20)
		with self.assertRaises(TypeError):
			dist1 < dist2
			
		dist3 = Distance("euclidean", 50, 75)
		_ = dist3.distance_calculator()
		
		with self.assertRaises(ValueError):
			dist1 < dist3
			
		#manhattan
		args1 = [7,8,10]
		args2 = [-7,8,9]
		md1 = Distance("manhattan",*args1)
		md2 = Distance("manhattan",*args2)
		_ = md1.distance_calculator()
		_ = md2.distance_calculator()	
		self.assertTrue(md2 < md1)
		
		#euclidean
		args1 = [12,17]
		args2 = [-12,16]
		ed1 = Distance("euclidean",*args1)
		ed2 = Distance("euclidean",*args2)
		_ = ed1.distance_calculator()
		_ = ed2.distance_calculator()
		self.assertTrue(ed2 < ed1)
		
		#cosine
		args1 = [8, 8]
		args2 = [8, 4]
		cd1 = Distance("cosine", *args1)
		cd2 = Distance("cosine", *args2)
		_ = cd1.distance_calculator()
		_ = cd2.distance_calculator()
		self.assertTrue(cd2 < cd1)
		
	def test_greater_equal_than(self):
		dist1 = Distance("euclidean", 30, 40)
		dist2 = Distance("cosine", 10, 20)
		with self.assertRaises(TypeError):
			dist1 >= dist2
			
		dist3 = Distance("euclidean", 50, 75)
		_ = dist3.distance_calculator()
		
		with self.assertRaises(ValueError):
			dist1 >= dist3
			
		#manhattan
		args1 = [7,8,10]
		args2 = [-7,8,9]
		args3 = [7,8,-10]
		md1 = Distance("manhattan",*args1)
		md2 = Distance("manhattan",*args2)
		md3 = Distance("manhattan",*args3)
		_ = md1.distance_calculator()
		_ = md2.distance_calculator()
		_ = md3.distance_calculator()	
		self.assertTrue(md1 >= md2)
		self.assertTrue(md1 >= md3)
		
		#euclidean
		args1 = [12,17]
		args2 = [-12,16]
		args3 = [12, -17]
		ed1 = Distance("euclidean",*args1)
		ed2 = Distance("euclidean",*args2)
		ed3 = Distance("euclidean",*args3)
		_ = ed1.distance_calculator()
		_ = ed2.distance_calculator()
		_ = ed3.distance_calculator()
		self.assertTrue(ed1 >= ed2)
		self.assertTrue(ed1 >= ed3)
		
		#cosine
		args1 = [8, 8]
		args2 = [8, 4]
		args3 = [7, 7]
		cd1 = Distance("cosine", *args1)
		cd2 = Distance("cosine", *args2)
		cd3 = Distance("cosine", *args3)
		_ = cd1.distance_calculator()
		_ = cd2.distance_calculator()
		_ = cd3.distance_calculator()
		self.assertTrue(cd1 >= cd2)
		self.assertTrue(cd1 >= cd3)
		
	def test_lesser_equal_than(self):
		dist1 = Distance("euclidean", 30, 40)
		dist2 = Distance("cosine", 10, 20)
		with self.assertRaises(TypeError):
			dist1 <= dist2
			
		dist3 = Distance("euclidean", 50, 75)
		_ = dist3.distance_calculator()
		
		with self.assertRaises(ValueError):
			dist1 <= dist3
			
		#manhattan
		args1 = [7,8,10]
		args2 = [-7,8,9]
		args3 = [7,8,-10]
		md1 = Distance("manhattan",*args1)
		md2 = Distance("manhattan",*args2)
		md3 = Distance("manhattan",*args3)
		_ = md1.distance_calculator()
		_ = md2.distance_calculator()
		_ = md3.distance_calculator()	
		self.assertTrue(md2 <= md1)
		self.assertTrue(md1 <= md3)
		
		#euclidean
		args1 = [12,17]
		args2 = [-12,16]
		args3 = [12, -17]
		ed1 = Distance("euclidean",*args1)
		ed2 = Distance("euclidean",*args2)
		ed3 = Distance("euclidean",*args3)
		_ = ed1.distance_calculator()
		_ = ed2.distance_calculator()
		_ = ed3.distance_calculator()
		self.assertTrue(ed2 <= ed1)
		self.assertTrue(ed1 <= ed3)
		
		#cosine
		args1 = [8, 8]
		args2 = [8, 4]
		args3 = [7, 7]
		cd1 = Distance("cosine", *args1)
		cd2 = Distance("cosine", *args2)
		cd3 = Distance("cosine", *args3)
		_ = cd1.distance_calculator()
		_ = cd2.distance_calculator()
		_ = cd3.distance_calculator()
		self.assertTrue(cd2 <= cd1)
		self.assertTrue(cd1 <= cd3)
		
		
		
		
		
		
		