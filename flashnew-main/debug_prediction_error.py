#!/usr/bin/env python3
"""
Debug the prediction error
"""

# Test type conversion directly
from type_converter_simple import TypeConverter

test_data = {
    "total_capital_raised_usd": 5000000,
    "funding_stage": "Series A",
    "has_strategic_partnerships": True,
    "tech_differentiation_score": 4,
    "product_retention_30d": 85,  # This might be the issue - sent as percentage
}

converter = TypeConverter()
try:
    converted = converter.convert_frontend_to_backend(test_data)
    print("Conversion successful!")
    print(f"Converted data: {converted}")
    
    # Check specific conversions
    print(f"\nConversions:")
    print(f"  funding_stage: '{test_data['funding_stage']}' → '{converted.get('funding_stage', 'MISSING')}'")
    print(f"  has_strategic_partnerships: {test_data['has_strategic_partnerships']} → {converted.get('has_strategic_partnerships', 'MISSING')}")
    print(f"  product_retention_30d: {test_data['product_retention_30d']} → {converted.get('product_retention_30d', 'MISSING')}")
    
except Exception as e:
    print(f"Conversion error: {e}")
    import traceback
    traceback.print_exc()