import { Box, Heading, HStack, Image, Text, VStack } from "@chakra-ui/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import React from "react";

const Card = ({ title, description, imageSrc }) => {
  // Implement the UI for the Card component according to the instructions.
  // You should be able to implement the component with the elements imported above.
  // Feel free to import other UI components from Chakra UI if you wish to.
  return (
    <>
      <Box color="#000" borderRadius="md" bg="#fff">
        <VStack>
          <Image src={imageSrc} alt={description} borderRadius="md"/>
          <Box textAlign="left" p="4">
            <Heading size="sm" mb="3">{title}</Heading>
            <Text fontSize="sm" mb="2">{description}</Text>
            <Text fontSize="sm">See more <FontAwesomeIcon icon={faArrowRight} size="1x" /></Text>
          </Box>
        </VStack>
      </Box>
    </>
  );
};

export default Card;
