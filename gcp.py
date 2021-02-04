#Importing required libraries
import googleapiclient.discovery

#Fuction to create a new project.
def create_project(crm, project_id, name):
    config = {
    'project_id' : project_id,
    'name' : name }
    return crm.projects().create(body = config).execute()

#Function to list all the projects.
def list_projects(crm):
    projects = crm.projects().list().execute()
    projects = projects.values()
    return projects


#Function which specifies which type of operating system instance is created.
def disk_image(project, family):

    image_response = compute.images().getFromFamily(
             project=project, family=family).execute()
    source_disk_image = image_response['selfLink']
    return source_disk_image

#Function to create a vm instance in google cloud.
def create_instance(compute, project, zone, name, image):
         # Configure the machine
    machine_type = "zones/%s/machineTypes/e2-standard-2" % zone
    config = {
        'name': name,
        'machineType': machine_type,
        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': image,
                }
            }
        ],
        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
    }
    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


#Function to list all the instances in a project.
def list_instance(compute, zone = 'us-central1-a',  project = 'hazel-logic-302608'):
    result = compute.instances().list(project=project, zone = zone).execute()
    return result['items'] if 'items' in result else none

#Function to delete an instance in a project.
def delete_instance(compute, name, project =  'hazel-logic-302608', zone = 'us-central1-a'):
    return compute.instances().delete(project = project, zone = zone, instance = name).execute()

if __name__ == '__main__':

    while True:
        print('''What do you want to do?
            1. Create Instance,
            2. List Instance,
            3. Delete Instance,
            4. List Projects,
            5. Create Project''')

        val = int(input("Enter what you want to do? "))

        crm = googleapiclient.discovery.build('cloudresourcemanager', 'v1')

        compute = googleapiclient.discovery.build('compute', 'v1')

        if val == 1:

            project_id = input("Enter project id :")

            name = input("Name of the Instance : ")
            zone = input("Zone :")
            os_project = input("OS Image Name :  (All supported images : https://cloud.google.com/compute/docs/images/os-details#general-info)" )
            os_family = input("OS family name :  (All supported images : https://cloud.google.com/compute/docs/images/os-details#general-info)")
            image = disk_image(os_project, os_family)
            print(create_instance(compute, project_id, zone, name, image))
            print('Your Instance has been created!')

        elif val == 2:

            project_id = input("Enter project id :")

            zone = input('Zone :')
            zone_val = zone.split(",")

            for i in zone_val:
                x = list_instance(compute, zone = i, project = project_id)
                for j in x:
                    print(f"{j['name']}  {j['zone']}")

        elif val == 3:

            project_id = input("Enter project id :")

            name = input("Name of the Instance that you want to delete : ")
            zone = input("Zone of the Instance to be deleted : ")

            print(delete_instance(compute, name, project_id, zone))
            print(f'{name} has been deleted!')
        elif val == 4:

            projects = list_projects(crm)
            for i in projects:
                for j in projects:
                    print(f"{j['name']}   {j['projectId']}")
            

        elif val ==5:

            name = input("Enter new Project Name : ")
            id = input("Enter new project ID : ")

            create_project(compute, id, name)
            print("{name} Project is created.")

        else:
            print("Please provide a valid option.")
