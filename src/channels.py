from error import InputError
import auth
import other

# Provide a list of all channels (and their associated details) 
# that the authorised user is part of:
def channels_list(token):
    # User of interest
    user_uid = token_to_uid(token)
    # Total number of channels  
    total_channels = len(other.data['channels'])
    # Output (Mimics data stucture already put in place)
    user_channels = {
                'channels': [],
            }
    
    for i in range(total_channels):
        if user_uid in other.data['channels'][i]['all_members']:
            user_channels['channels'].append(other.data['channels'][i])
            
    return user_channels


# Provide a list of all channels (and their associated details)
def channels_listall(token):
    # Simply return data strcture which stores all channel information. 
    return other.data

# Creates a new channel with that name that is either 
# a public or private channel
def channels_create(token, name, is_public):
    # First check to see if inputted name is valid:
    # Cannot be greater than 20 characters long 
    if len(name) > 20:
        raise InputError('Channel name is greater than 20 characters long - Cannot create channel')
    # Cannot be left blank 
    if len(name) == 0:
        raise InputError('Field, "Channel name" left blank - Cannot create channel')
    # Name cannot already exist 
    total_channels = len(other.data['channels'])
    user_uid = token_to_uid(token)
    for i in range(total_channels):
        if name in other.data['channels'][i]['channel_name']:
            raise InputError('Channel name already exists - Cannot create channel')
    
    # Testing if this is the first channel being created. 
    if not other.data['channels']: 
        channel_id = 1 
    else:
        channel_id = len(other.data['channels'])

    # Assumtpion: When a channel is created the creator becomes owner by default 
    # (Will be added to assumptions)
    new_channel = {
            'channel_name': name,  
            'channel_id': channel_id,
            'is_public': is_public,
            'owner_members': [token_to_uid(token),],
            'all_members': [token_to_uid(token),],
    }   

    other.data['channels'].append(new_channel)
   
    return {
        'channel_id': channel_id,
    }

# Coverts the users token to a valid user_id 
def token_to_uid(token):
    for user in other.data['users']:
        if user['token'] == token:
            return user['u_id']
    else:
        return -1 
