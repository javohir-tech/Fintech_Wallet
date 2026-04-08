from rest_framework import serializers

class RegisterEmialorNumberSerializers(serializers.Serializer):
    user_input = serializers.CharField(max_length = 128 )
    
    def validate(self, attrs):
        temp_input = attrs['user_input']
        print("="*50)
        print(temp_input)
        print("="*50)