import pytest
from src.database_objects.schema_builder import SchemaBuilder

class TestSchemaBuilder:
    def test_Build_WithNestedTableBuilders_ShouldReturnPopulatedSchema(self):
        sb = SchemaBuilder("ecommerce")
        
        # Nested execution 1
        (sb.with_table("users")
           .with_int_column("id")
           .with_string_column("username", 50))
           
        # Nested execution 2
        (sb.with_table("orders")
           .with_int_column("order_id"))
           
        # Build triggering cascade
        schema = sb.build()
        
        assert schema.name == "ecommerce"
        assert schema.contains_table("users") is True
        assert schema.contains_table("orders") is True
        
        # Verify deeper levels (Table -> Column) were built properly
        assert schema.get_table("users").contains_column("username") is True
        assert schema.get_table("orders").contains_column("order_id") is True
