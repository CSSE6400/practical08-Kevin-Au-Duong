resource "docker_image" "taskoverflow" { 
 name = "${aws_ecr_repository.taskoverflow.repository_url}:latest" 
 build { 
   context = "." 
 } 
} 

resource "docker_registry_image" "taskoverflow" { 
 name = docker_image.taskoverflow.name 
}

