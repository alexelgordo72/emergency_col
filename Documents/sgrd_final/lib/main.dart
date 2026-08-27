import 'package:flutter/material.dart';
import 'package:sgrd_final/screens/principal.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SGRD Yumbo',
      theme: ThemeData(
        primarySwatch: Colors.red,
        useMaterial3: true,
      ),
      home: const Principal(),
      debugShowCheckedModeBanner: false,
    );
  }
}
